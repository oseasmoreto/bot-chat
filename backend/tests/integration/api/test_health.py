import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from api.contexts.health.application.get_health import AppInfo, GetHealthUseCase
from api.contexts.health.domain.value_objects import HealthStatus
from api.contexts.health.presentation.dependencies import get_health_use_case
from tests.fakes import STARTED_AT, FakeClock, StubCheck

EXPECTED_FIELDS = {"status", "scope", "version", "uptimeSeconds", "checkedAt", "components"}


def override_checks(app: FastAPI, *checks: StubCheck) -> None:
    use_case = GetHealthUseCase(
        clock=FakeClock(STARTED_AT),
        app_info=AppInfo(version="test", started_at=STARTED_AT),
        checks=checks,
    )
    app.dependency_overrides[get_health_use_case] = lambda: use_case


@pytest.mark.parametrize("scope", ["public", "admin"])
async def test_health_returns_ok_for_scope(client: AsyncClient, scope: str) -> None:
    response = await client.get(f"/api/v1/{scope}/health")

    assert response.status_code == 200
    body = response.json()
    assert set(body) == EXPECTED_FIELDS
    assert body["status"] == "ok"
    assert body["scope"] == scope
    assert body["version"] == "test"
    assert body["components"] == []


@pytest.mark.parametrize("scope", ["public", "admin"])
async def test_health_returns_200_when_a_component_is_degraded(
    app: FastAPI, client: AsyncClient, scope: str
) -> None:
    override_checks(app, StubCheck("partner:acme", HealthStatus.DEGRADED))

    response = await client.get(f"/api/v1/{scope}/health")

    assert response.status_code == 200
    assert response.json()["status"] == "degraded"
    assert response.json()["components"] == [
        {"name": "partner:acme", "status": "degraded", "detail": None}
    ]


@pytest.mark.parametrize("scope", ["public", "admin"])
async def test_health_returns_503_when_a_component_is_down(
    app: FastAPI, client: AsyncClient, scope: str
) -> None:
    override_checks(app, StubCheck("database", HealthStatus.DOWN))

    response = await client.get(f"/api/v1/{scope}/health")

    assert response.status_code == 503
    assert response.json()["status"] == "down"
