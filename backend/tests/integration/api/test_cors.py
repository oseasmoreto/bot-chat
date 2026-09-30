from httpx import AsyncClient

from tests.conftest import ALLOWED_ORIGIN


async def test_preflight_allows_configured_origin(client: AsyncClient) -> None:
    response = await client.options(
        "/api/v1/public/health",
        headers={"Origin": ALLOWED_ORIGIN, "Access-Control-Request-Method": "GET"},
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED_ORIGIN
    assert response.headers["access-control-allow-credentials"] == "true"


async def test_preflight_rejects_unknown_origin(client: AsyncClient) -> None:
    response = await client.options(
        "/api/v1/admin/health",
        headers={"Origin": "https://malicioso.example", "Access-Control-Request-Method": "GET"},
    )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


async def test_response_exposes_request_id_to_allowed_origin(client: AsyncClient) -> None:
    response = await client.get("/api/v1/public/health", headers={"Origin": ALLOWED_ORIGIN})

    assert response.headers["access-control-allow-origin"] == ALLOWED_ORIGIN
    assert response.headers["access-control-expose-headers"] == "X-Request-ID"


async def test_response_has_no_cors_header_for_unknown_origin(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/public/health", headers={"Origin": "https://malicioso.example"}
    )

    assert "access-control-allow-origin" not in response.headers
