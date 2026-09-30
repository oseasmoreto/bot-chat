import pytest
from httpx import AsyncClient


async def test_generates_request_id_when_absent(client: AsyncClient) -> None:
    response = await client.get("/api/v1/public/health")

    assert len(response.headers["x-request-id"]) == 32


async def test_propagates_valid_request_id(client: AsyncClient) -> None:
    response = await client.get("/api/v1/public/health", headers={"X-Request-ID": "front-123"})

    assert response.headers["x-request-id"] == "front-123"


@pytest.mark.parametrize("invalid", ["tem espaco", "a" * 129, "quebra\\nlinha"])
async def test_replaces_invalid_request_id(client: AsyncClient, invalid: str) -> None:
    response = await client.get("/api/v1/public/health", headers={"X-Request-ID": invalid})

    assert response.headers["x-request-id"] != invalid
    assert len(response.headers["x-request-id"]) == 32
