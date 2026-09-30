from typing import Annotated

import pytest
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from httpx import AsyncClient

from api.core.exceptions import ConflictError, DomainError, NotFoundError

REQUEST_ID = {"X-Request-ID": "req-1"}


@pytest.fixture
def app_with_error_routes(app: FastAPI) -> FastAPI:
    """Rotas só de teste que disparam cada tipo de erro."""

    @app.get("/test/not-found")
    async def raise_not_found() -> None:
        raise NotFoundError("Parceiro não encontrado")

    @app.get("/test/conflict")
    async def raise_conflict() -> None:
        raise ConflictError("Parceiro alterado por outra operação")

    @app.get("/test/domain")
    async def raise_domain() -> None:
        raise DomainError("Regra violada")

    @app.get("/test/validation")
    async def validate(limit: Annotated[int, Query(ge=1)]) -> int:
        return limit

    @app.get("/test/crash")
    async def crash() -> None:
        raise RuntimeError("detalhe interno")

    return app


async def test_unknown_route_returns_standard_not_found(client: AsyncClient) -> None:
    response = await client.get("/api/v1/public/nao-existe", headers=REQUEST_ID)

    assert response.status_code == 404
    assert response.json() == {
        "error": {"code": "not_found", "message": "Recurso não encontrado", "requestId": "req-1"}
    }


async def test_wrong_method_returns_method_not_allowed(client: AsyncClient) -> None:
    response = await client.post("/api/v1/public/health")

    assert response.status_code == 405
    assert response.json()["error"]["code"] == "method_not_allowed"


@pytest.mark.parametrize(
    ("path", "status_code", "code", "message"),
    [
        ("/test/not-found", 404, "not_found", "Parceiro não encontrado"),
        ("/test/conflict", 409, "conflict", "Parceiro alterado por outra operação"),
        ("/test/domain", 422, "domain_error", "Regra violada"),
    ],
)
async def test_domain_errors_use_standard_format(
    app_with_error_routes: FastAPI,
    client: AsyncClient,
    path: str,
    status_code: int,
    code: str,
    message: str,
) -> None:
    response = await client.get(path, headers=REQUEST_ID)

    assert response.status_code == status_code
    assert response.json() == {"error": {"code": code, "message": message, "requestId": "req-1"}}


async def test_validation_error_lists_invalid_fields(
    app_with_error_routes: FastAPI, client: AsyncClient
) -> None:
    response = await client.get("/test/validation?limit=0")

    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "validation_error"
    assert error["details"] == [
        {"field": "query.limit", "message": "Input should be greater than or equal to 1"}
    ]


def test_unexpected_error_hides_internal_details(
    app_with_error_routes: FastAPI, caplog: pytest.LogCaptureFixture
) -> None:
    with TestClient(app_with_error_routes, raise_server_exceptions=False) as http:
        response = http.get("/test/crash", headers=REQUEST_ID)

    assert response.status_code == 500
    assert response.json() == {
        "error": {"code": "internal_error", "message": "Erro interno", "requestId": "req-1"}
    }
    assert "detalhe interno" not in response.text
    assert "http.unhandled_error" in caplog.messages
