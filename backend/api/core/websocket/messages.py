from typing import Any

from pydantic import Field

from api.core.schemas import BaseSchema


class WsMessage(BaseSchema):
    type: str
    id: str | None = None
    # Any só na fronteira: cada handler valida o próprio payload.
    payload: dict[str, Any] = Field(default_factory=dict)


def ws_error(code: str, message: str, *, request_id: str | None = None) -> WsMessage:
    return WsMessage(type="error", id=request_id, payload={"code": code, "message": message})
