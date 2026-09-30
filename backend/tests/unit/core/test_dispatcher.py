import pytest

from api.core.scope import Scope
from api.core.websocket.dispatcher import MessageDispatcher
from api.core.websocket.messages import WsMessage


async def echo(message: WsMessage, scope: Scope) -> WsMessage:
    return WsMessage(type="echo", id=message.id, payload={"scope": scope.value})


async def test_dispatch_calls_registered_handler_with_scope() -> None:
    dispatcher = MessageDispatcher()
    dispatcher.register("test.echo", echo)

    reply = await dispatcher.dispatch(WsMessage(type="test.echo", id="1"), Scope.ADMIN)

    assert reply == WsMessage(type="echo", id="1", payload={"scope": "admin"})


async def test_dispatch_returns_error_for_unknown_type() -> None:
    reply = await MessageDispatcher().dispatch(WsMessage(type="nope", id="7"), Scope.PUBLIC)

    assert reply.type == "error"
    assert reply.id == "7"
    assert reply.payload["code"] == "unknown_message_type"


def test_register_rejects_duplicated_type() -> None:
    dispatcher = MessageDispatcher()
    dispatcher.register("test.echo", echo)

    with pytest.raises(ValueError, match=r"test\.echo"):
        dispatcher.register("test.echo", echo)
