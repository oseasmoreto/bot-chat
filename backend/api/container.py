from dataclasses import dataclass
from datetime import UTC, datetime

from fastapi.requests import HTTPConnection

from api.config import Settings
from api.contexts.health.application.get_health import AppInfo, GetHealthUseCase
from api.contexts.health.infrastructure.system_clock import SystemClock
from api.contexts.health.presentation.ws_handlers import HealthPingHandler
from api.core.websocket.dispatcher import MessageDispatcher


@dataclass(frozen=True, slots=True)
class Container:
    settings: Settings
    get_health: GetHealthUseCase
    ws_dispatcher: MessageDispatcher


def build_container(settings: Settings) -> Container:
    get_health = GetHealthUseCase(
        clock=SystemClock(),
        app_info=AppInfo(version=settings.version, started_at=datetime.now(UTC)),
        checks=(),  # futuros: DynamoDbHealthCheck(...) (docs/12), PartnerApiHealthCheck(...)
    )
    dispatcher = MessageDispatcher()
    dispatcher.register("health.ping", HealthPingHandler(get_health))
    return Container(settings=settings, get_health=get_health, ws_dispatcher=dispatcher)


def get_container(connection: HTTPConnection) -> Container:
    """Dependency do FastAPI. Funciona tanto para requisições HTTP quanto WebSocket."""
    container: Container = connection.app.state.container
    return container
