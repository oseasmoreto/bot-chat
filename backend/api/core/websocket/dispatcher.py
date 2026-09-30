from collections.abc import Awaitable, Callable

from api.core.scope import Scope
from api.core.websocket.messages import WsMessage, ws_error

WsHandler = Callable[[WsMessage, Scope], Awaitable[WsMessage]]


class MessageDispatcher:
    def __init__(self) -> None:
        self._handlers: dict[str, WsHandler] = {}

    def register(self, message_type: str, handler: WsHandler) -> None:
        if message_type in self._handlers:
            raise ValueError(f"Handler já registrado para '{message_type}'")
        self._handlers[message_type] = handler

    async def dispatch(self, message: WsMessage, scope: Scope) -> WsMessage:
        handler = self._handlers.get(message.type)
        if handler is None:
            return ws_error(
                "unknown_message_type",
                f"Tipo de mensagem não suportado: {message.type}",
                request_id=message.id,
            )
        return await handler(message, scope)
