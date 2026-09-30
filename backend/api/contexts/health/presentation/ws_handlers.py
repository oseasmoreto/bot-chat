from api.contexts.health.application.get_health import GetHealthUseCase
from api.contexts.health.presentation.schemas import HealthResponse
from api.core.scope import Scope
from api.core.websocket.messages import WsMessage


class HealthPingHandler:
    def __init__(self, use_case: GetHealthUseCase) -> None:
        self._use_case = use_case

    async def __call__(self, message: WsMessage, scope: Scope) -> WsMessage:
        report = await self._use_case.execute(scope)
        return WsMessage(
            type="health.pong",
            id=message.id,
            payload=HealthResponse.from_domain(report).model_dump(mode="json", by_alias=True),
        )
