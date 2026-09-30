import logging
from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from pydantic import ValidationError

from api.container import Container, get_container
from api.core.scope import Scope
from api.core.websocket.messages import WsMessage, ws_error

logger = logging.getLogger(__name__)
ws_router = APIRouter()


async def serve_socket(websocket: WebSocket, scope: Scope, container: Container) -> None:
    # CORS não se aplica a WebSocket: o navegador conecta de qualquer origem.
    # Validamos o Origin no handshake para impedir Cross-Site WebSocket Hijacking.
    if websocket.headers.get("origin") not in container.settings.cors_origins:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        logger.warning("ws.rejected_origin", extra={"scope": scope.value})
        return

    await websocket.accept()
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                message = WsMessage.model_validate_json(raw)
            except ValidationError:
                reply = ws_error("invalid_message", "Envelope inválido")
            else:
                reply = await container.ws_dispatcher.dispatch(message, scope)
            await websocket.send_text(reply.model_dump_json(by_alias=True))
    except WebSocketDisconnect:
        logger.info("ws.disconnected", extra={"scope": scope.value})


@ws_router.websocket("/api/v1/ws/public")
async def public_socket(
    websocket: WebSocket, container: Annotated[Container, Depends(get_container)]
) -> None:
    await serve_socket(websocket, Scope.PUBLIC, container)


@ws_router.websocket("/api/v1/ws/admin")
async def admin_socket(
    websocket: WebSocket, container: Annotated[Container, Depends(get_container)]
) -> None:
    await serve_socket(websocket, Scope.ADMIN, container)
