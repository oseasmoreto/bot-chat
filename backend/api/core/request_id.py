import re
from contextvars import ContextVar
from typing import Final
from uuid import uuid4

from starlette.datastructures import MutableHeaders
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Message, Receive, Scope, Send

REQUEST_ID_HEADER: Final = "X-Request-ID"
# Valor recebido de fora só é reaproveitado se for curto e sem caracteres especiais
# (evita injeção no log e em headers).
_VALID_REQUEST_ID: Final = re.compile(r"^[A-Za-z0-9._-]{1,128}$")

request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)


def get_request_id(connection: HTTPConnection) -> str | None:
    """Request ID da requisição/conexão atual (definido pelo RequestIdMiddleware)."""
    request_id: str | None = connection.scope.get("state", {}).get("request_id")
    return request_id


def _resolve(incoming: str | None) -> str:
    if incoming and _VALID_REQUEST_ID.fullmatch(incoming):
        return incoming
    return uuid4().hex


class RequestIdMiddleware:
    """Gera ou propaga o X-Request-ID e o devolve na resposta.

    ASGI puro (e não BaseHTTPMiddleware) para funcionar também no handshake do WebSocket.
    """

    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in {"http", "websocket"}:
            await self._app(scope, receive, send)
            return

        request_id = _resolve(HTTPConnection(scope).headers.get(REQUEST_ID_HEADER))
        scope.setdefault("state", {})["request_id"] = request_id
        token = request_id_var.set(request_id)

        async def send_with_request_id(message: Message) -> None:
            if message["type"] == "http.response.start":
                MutableHeaders(scope=message)[REQUEST_ID_HEADER] = request_id
            await send(message)

        try:
            await self._app(scope, receive, send_with_request_id)
        finally:
            request_id_var.reset(token)
