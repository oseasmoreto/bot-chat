# Backend — Testes

> Estratégia geral (TDD, pirâmide, matriz obrigatória, cobertura) em [05 — Estratégia de testes](../05-estrategia-testes.md).

## `tests/fakes.py` e `tests/conftest.py`

```python
# tests/fakes.py — dublês que implementam as ports (Protocol) do domínio
from datetime import UTC, datetime

from bot_varejo.contexts.health.domain.entities import ComponentHealth
from bot_varejo.contexts.health.domain.value_objects import HealthStatus

STARTED_AT = datetime(2026, 1, 1, tzinfo=UTC)


class FakeClock:
    def __init__(self, now: datetime) -> None:
        self._now = now

    def now(self) -> datetime:
        return self._now


class StubCheck:
    def __init__(self, name: str, status: HealthStatus) -> None:
        self.name = name
        self._status = status

    async def check(self) -> ComponentHealth:
        return ComponentHealth(name=self.name, status=self._status)
```

```python
# tests/conftest.py
from collections.abc import AsyncIterator, Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from bot_varejo.core.config import Settings
from bot_varejo.main import create_app


@pytest.fixture
def app() -> FastAPI:
    return create_app(Settings(env="local", version="test"))


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
        yield http


@pytest.fixture
def ws_client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
```

## Unitário — caso de uso

```python
from datetime import timedelta

import pytest

from bot_varejo.core.scope import Scope
from bot_varejo.contexts.health.application.get_health import AppInfo, GetHealthUseCase
from bot_varejo.contexts.health.domain.value_objects import HealthStatus
from tests.fakes import STARTED_AT, FakeClock, StubCheck


async def test_returns_ok_when_there_are_no_checks() -> None:
    use_case = GetHealthUseCase(
        clock=FakeClock(STARTED_AT + timedelta(seconds=10)),
        app_info=AppInfo(version="1.0.0", started_at=STARTED_AT),
    )

    report = await use_case.execute(Scope.PUBLIC)

    assert report.status is HealthStatus.OK
    assert report.scope is Scope.PUBLIC
    assert report.uptime_seconds == 10


@pytest.mark.parametrize(
    ("statuses", "expected"),
    [
        ([HealthStatus.OK, HealthStatus.OK], HealthStatus.OK),
        ([HealthStatus.OK, HealthStatus.DEGRADED], HealthStatus.DEGRADED),
        ([HealthStatus.DEGRADED, HealthStatus.DOWN], HealthStatus.DOWN),
    ],
)
async def test_returns_worst_component_status(
    statuses: list[HealthStatus], expected: HealthStatus
) -> None:
    checks = [StubCheck(f"dep{i}", status) for i, status in enumerate(statuses)]
    use_case = GetHealthUseCase(
        clock=FakeClock(STARTED_AT),
        app_info=AppInfo(version="1.0.0", started_at=STARTED_AT),
        checks=checks,
    )

    report = await use_case.execute(Scope.ADMIN)

    assert report.status is expected
    assert len(report.components) == len(statuses)
```

## Integração — rota HTTP (os dois escopos)

```python
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from bot_varejo.contexts.health.application.get_health import AppInfo, GetHealthUseCase
from bot_varejo.contexts.health.domain.value_objects import HealthStatus
from bot_varejo.contexts.health.presentation.dependencies import get_health_use_case
from tests.fakes import STARTED_AT, FakeClock, StubCheck

EXPECTED_FIELDS = {"status", "scope", "version", "uptimeSeconds", "checkedAt", "components"}


@pytest.mark.parametrize("scope", ["public", "admin"])
async def test_health_returns_ok_for_scope(client: AsyncClient, scope: str) -> None:
    response = await client.get(f"/api/v1/{scope}/health")

    assert response.status_code == 200
    body = response.json()
    assert set(body) == EXPECTED_FIELDS
    assert body["status"] == "ok"
    assert body["scope"] == scope
    assert body["version"] == "test"


async def test_health_returns_503_when_a_component_is_down(
    app: FastAPI, client: AsyncClient
) -> None:
    down_use_case = GetHealthUseCase(
        clock=FakeClock(STARTED_AT),
        app_info=AppInfo(version="test", started_at=STARTED_AT),
        checks=[StubCheck("database", HealthStatus.DOWN)],
    )
    app.dependency_overrides[get_health_use_case] = lambda: down_use_case

    response = await client.get("/api/v1/public/health")

    assert response.status_code == 503
    assert response.json()["status"] == "down"
```

## Integração — WebSocket

```python
import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize("scope", ["public", "admin"])
def test_ping_returns_pong_with_same_id(ws_client: TestClient, scope: str) -> None:
    with ws_client.websocket_connect(f"/ws/{scope}") as ws:
        ws.send_json({"type": "health.ping", "id": "abc", "payload": {}})
        reply = ws.receive_json()

    assert reply["type"] == "health.pong"
    assert reply["id"] == "abc"
    assert reply["payload"]["scope"] == scope


def test_unknown_type_returns_error(ws_client: TestClient) -> None:
    with ws_client.websocket_connect("/ws/public") as ws:
        ws.send_json({"type": "nope", "id": "1", "payload": {}})
        reply = ws.receive_json()

    assert reply == {
        "type": "error",
        "id": "1",
        "payload": {"code": "unknown_message_type", "message": "Tipo de mensagem não suportado: nope"},
    }


def test_invalid_json_returns_error(ws_client: TestClient) -> None:
    with ws_client.websocket_connect("/ws/public") as ws:
        ws.send_text("não é json")
        reply = ws.receive_json()

    assert reply["payload"]["code"] == "invalid_message"
```

## Contrato — OpenAPI versionado

```python
import json
from pathlib import Path

from fastapi import FastAPI

OPENAPI_PATH = Path(__file__).parents[3] / "packages" / "api-client" / "openapi.json"


def test_committed_openapi_matches_backend(app: FastAPI) -> None:
    committed = json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))
    generated = app.openapi()

    # Compara só o contrato (paths + schemas); info.version varia por ambiente.
    assert generated["paths"] == committed["paths"], "Rode `make openapi`"
    assert generated["components"] == committed["components"], "Rode `make openapi`"
```
