import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from tests.conftest import ALLOWED_ORIGIN

ORIGIN = {"origin": ALLOWED_ORIGIN}
SCOPES = ["public", "admin"]


@pytest.mark.parametrize("scope", SCOPES)
def test_ping_returns_pong_with_same_id(ws_client: TestClient, scope: str) -> None:
    with ws_client.websocket_connect(f"/api/v1/ws/{scope}", headers=ORIGIN) as ws:
        ws.send_json({"type": "health.ping", "id": "abc", "payload": {}})
        reply = ws.receive_json()

    assert reply["type"] == "health.pong"
    assert reply["id"] == "abc"
    assert reply["payload"]["scope"] == scope
    assert reply["payload"]["status"] == "ok"
    assert "uptimeSeconds" in reply["payload"]


@pytest.mark.parametrize("scope", SCOPES)
def test_unknown_type_returns_error(ws_client: TestClient, scope: str) -> None:
    with ws_client.websocket_connect(f"/api/v1/ws/{scope}", headers=ORIGIN) as ws:
        ws.send_json({"type": "nope", "id": "1", "payload": {}})
        reply = ws.receive_json()

    assert reply == {
        "type": "error",
        "id": "1",
        "payload": {
            "code": "unknown_message_type",
            "message": "Tipo de mensagem não suportado: nope",
        },
    }


@pytest.mark.parametrize("raw", ["não é json", '{"id": "sem-type"}', '{"type": 1}'])
def test_invalid_envelope_returns_error(ws_client: TestClient, raw: str) -> None:
    with ws_client.websocket_connect("/api/v1/ws/public", headers=ORIGIN) as ws:
        ws.send_text(raw)
        reply = ws.receive_json()

    assert reply == {
        "type": "error",
        "id": None,
        "payload": {"code": "invalid_message", "message": "Envelope inválido"},
    }


def test_connection_keeps_serving_after_an_error(ws_client: TestClient) -> None:
    with ws_client.websocket_connect("/api/v1/ws/admin", headers=ORIGIN) as ws:
        ws.send_text("não é json")
        ws.receive_json()
        ws.send_json({"type": "health.ping", "id": "2"})
        reply = ws.receive_json()

    assert reply["type"] == "health.pong"


@pytest.mark.parametrize("scope", SCOPES)
@pytest.mark.parametrize("headers", [{}, {"origin": "https://malicioso.example"}])
def test_rejects_connection_from_unknown_origin(
    ws_client: TestClient, scope: str, headers: dict[str, str]
) -> None:
    with (
        pytest.raises(WebSocketDisconnect) as exc_info,
        ws_client.websocket_connect(f"/api/v1/ws/{scope}", headers=headers),
    ):
        pass

    assert exc_info.value.code == 1008  # policy violation
