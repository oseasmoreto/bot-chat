# Backend — Context `health` (código de referência)

> Exemplos que a implementação deve seguir. Nomes de arquivos batem com a árvore em [Estrutura de pastas do backend](./01-estrutura.md).

## `core/scope.py`

```python
from enum import StrEnum


class Scope(StrEnum):
    """Escopo de acesso da aplicação. Define prefixos de rota e regras futuras de auth."""

    PUBLIC = "public"
    ADMIN = "admin"
```

## `contexts/health/domain/value_objects.py`

```python
from collections.abc import Iterable
from enum import StrEnum
from typing import Final


class HealthStatus(StrEnum):
    OK = "ok"
    DEGRADED = "degraded"
    DOWN = "down"

    @classmethod
    def worst(cls, statuses: Iterable["HealthStatus"]) -> "HealthStatus":
        """Status agregado = o pior entre os componentes. Sem componentes → OK."""
        return max(statuses, key=_SEVERITY.__getitem__, default=cls.OK)


_SEVERITY: Final[dict[HealthStatus, int]] = {
    HealthStatus.OK: 0,
    HealthStatus.DEGRADED: 1,
    HealthStatus.DOWN: 2,
}
```

## `contexts/health/domain/entities.py`

```python
from dataclasses import dataclass
from datetime import datetime

from bot_varejo.core.scope import Scope
from bot_varejo.contexts.health.domain.value_objects import HealthStatus


@dataclass(frozen=True, slots=True, kw_only=True)
class ComponentHealth:
    name: str
    status: HealthStatus
    detail: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class HealthReport:
    scope: Scope
    status: HealthStatus
    version: str
    uptime_seconds: float
    checked_at: datetime
    components: tuple[ComponentHealth, ...] = ()
```

## `contexts/health/domain/ports.py`

```python
from datetime import datetime
from typing import Protocol

from bot_varejo.contexts.health.domain.entities import ComponentHealth


class ClockPort(Protocol):
    def now(self) -> datetime: ...


class HealthCheckPort(Protocol):
    """Verificação de uma dependência (ex.: banco, cache, API de parceiro)."""

    @property
    def name(self) -> str: ...

    async def check(self) -> ComponentHealth: ...
```

## `contexts/health/application/get_health.py`

```python
import asyncio
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

from bot_varejo.core.scope import Scope
from bot_varejo.contexts.health.domain.entities import HealthReport
from bot_varejo.contexts.health.domain.ports import ClockPort, HealthCheckPort
from bot_varejo.contexts.health.domain.value_objects import HealthStatus


@dataclass(frozen=True, slots=True)
class AppInfo:
    version: str
    started_at: datetime


class GetHealthUseCase:
    def __init__(
        self,
        *,
        clock: ClockPort,
        app_info: AppInfo,
        checks: Sequence[HealthCheckPort] = (),
    ) -> None:
        self._clock = clock
        self._app_info = app_info
        self._checks = tuple(checks)

    async def execute(self, scope: Scope) -> HealthReport:
        components = tuple(await asyncio.gather(*(c.check() for c in self._checks)))
        now = self._clock.now()
        return HealthReport(
            scope=scope,
            status=HealthStatus.worst(c.status for c in components),
            version=self._app_info.version,
            uptime_seconds=(now - self._app_info.started_at).total_seconds(),
            checked_at=now,
            components=components,
        )
```

## `contexts/health/infrastructure/system_clock.py`

```python
from datetime import UTC, datetime


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)
```

## `core/schemas.py` — base de todos os DTOs

```python
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    """Python usa snake_case; o JSON exposto usa camelCase (ADR-0008)."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        frozen=True,
    )
```

## `contexts/health/presentation/schemas.py`

```python
from datetime import datetime
from typing import Self

from bot_varejo.core.schemas import BaseSchema
from bot_varejo.core.scope import Scope
from bot_varejo.contexts.health.domain.entities import HealthReport
from bot_varejo.contexts.health.domain.value_objects import HealthStatus


class ComponentHealthResponse(BaseSchema):
    name: str
    status: HealthStatus
    detail: str | None = None


class HealthResponse(BaseSchema):
    status: HealthStatus
    scope: Scope
    version: str
    uptime_seconds: float
    checked_at: datetime
    components: list[ComponentHealthResponse]

    @classmethod
    def from_domain(cls, report: HealthReport) -> Self:
        return cls(
            status=report.status,
            scope=report.scope,
            version=report.version,
            uptime_seconds=report.uptime_seconds,
            checked_at=report.checked_at,
            components=[
                ComponentHealthResponse(name=c.name, status=c.status, detail=c.detail)
                for c in report.components
            ],
        )
```

## `container.py` — composition root

```python
from dataclasses import dataclass
from datetime import UTC, datetime

from fastapi.requests import HTTPConnection

from bot_varejo.core.config import Settings
from bot_varejo.core.websocket.dispatcher import MessageDispatcher
from bot_varejo.contexts.health.application.get_health import AppInfo, GetHealthUseCase
from bot_varejo.contexts.health.infrastructure.system_clock import SystemClock
from bot_varejo.contexts.health.presentation.ws_handlers import HealthPingHandler


@dataclass(frozen=True, slots=True)
class Container:
    settings: Settings
    get_health: GetHealthUseCase
    ws_dispatcher: MessageDispatcher


def build_container(settings: Settings) -> Container:
    get_health = GetHealthUseCase(
        clock=SystemClock(),
        app_info=AppInfo(version=settings.version, started_at=datetime.now(UTC)),
        checks=(),  # futuros: DatabaseHealthCheck(...), PartnerApiHealthCheck(...)
    )
    dispatcher = MessageDispatcher()
    dispatcher.register("health.ping", HealthPingHandler(get_health))
    return Container(settings=settings, get_health=get_health, ws_dispatcher=dispatcher)


def get_container(connection: HTTPConnection) -> Container:
    """Dependency do FastAPI. Funciona tanto para requisições HTTP quanto WebSocket."""
    container: Container = connection.app.state.container
    return container
```

## `contexts/health/presentation/dependencies.py`

```python
from typing import Annotated

from fastapi import Depends

from bot_varejo.container import Container, get_container
from bot_varejo.contexts.health.application.get_health import GetHealthUseCase


def get_health_use_case(
    container: Annotated[Container, Depends(get_container)],
) -> GetHealthUseCase:
    return container.get_health
```

> Em testes, substituímos com `app.dependency_overrides[get_health_use_case] = lambda: fake_use_case`.

## `contexts/health/presentation/http.py` — router factory (DRY por escopo)

```python
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from bot_varejo.core.scope import Scope
from bot_varejo.contexts.health.application.get_health import GetHealthUseCase
from bot_varejo.contexts.health.domain.value_objects import HealthStatus
from bot_varejo.contexts.health.presentation.dependencies import get_health_use_case
from bot_varejo.contexts.health.presentation.schemas import HealthResponse


def build_health_router(scope: Scope) -> APIRouter:
    router = APIRouter(prefix="/health", tags=["health"])

    @router.get(
        "",
        summary=f"Health check do escopo {scope.value}",
        operation_id=f"get{scope.value.capitalize()}Health",
        responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": HealthResponse}},
    )
    async def get_health(
        response: Response,
        use_case: Annotated[GetHealthUseCase, Depends(get_health_use_case)],
    ) -> HealthResponse:
        report = await use_case.execute(scope)
        if report.status is HealthStatus.DOWN:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthResponse.from_domain(report)

    return router
```

## `api/public.py` e `api/admin.py`

```python
# api/public.py
from fastapi import APIRouter

from bot_varejo.core.scope import Scope
from bot_varejo.contexts.health.presentation.http import build_health_router

public_router = APIRouter(prefix="/api/v1/public", tags=["public"])
public_router.include_router(build_health_router(Scope.PUBLIC))
```

```python
# api/admin.py
from fastapi import APIRouter

from bot_varejo.core.scope import Scope
from bot_varejo.contexts.health.presentation.http import build_health_router

admin_router = APIRouter(prefix="/api/v1/admin", tags=["admin"])
admin_router.include_router(build_health_router(Scope.ADMIN))
# Futuro: dependencies=[Depends(require_admin)] quando o context identity existir.
```

## `main.py`

```python
from fastapi import FastAPI

from bot_varejo.api.admin import admin_router
from bot_varejo.api.public import public_router
from bot_varejo.api.websocket import ws_router
from bot_varejo.container import build_container
from bot_varejo.core.config import Settings
from bot_varejo.core.errors import register_error_handlers
from bot_varejo.core.logging import configure_logging


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title="Bot Varejo API",
        version=settings.version,
        docs_url="/api/docs" if settings.docs_enabled else None,
        redoc_url="/api/redoc" if settings.docs_enabled else None,
        openapi_url="/api/openapi.json" if settings.docs_enabled else None,
    )
    app.state.container = build_container(settings)

    app.include_router(public_router)
    app.include_router(admin_router)
    app.include_router(ws_router)
    register_error_handlers(app)
    return app
```

Execução: `uvicorn bot_varejo.main:create_app --factory --host 127.0.0.1 --port 8000`.

## `core/config.py`

```python
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

    env: Literal["local", "dev", "staging", "production"] = "local"
    version: str = "0.1.0"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    docs_enabled: bool = True
```

Todas as variáveis estão listadas em [04 — Docker §5](../04-docker-deploy.md#5-variáveis-de-ambiente).
