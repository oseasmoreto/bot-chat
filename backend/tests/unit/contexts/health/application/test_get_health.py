from datetime import timedelta

import pytest

from api.contexts.health.application.get_health import AppInfo, GetHealthUseCase
from api.contexts.health.domain.value_objects import HealthStatus
from api.core.scope import Scope
from tests.fakes import STARTED_AT, FakeClock, StubCheck


async def test_returns_ok_when_there_are_no_checks() -> None:
    use_case = GetHealthUseCase(
        clock=FakeClock(STARTED_AT + timedelta(seconds=10)),
        app_info=AppInfo(version="1.0.0", started_at=STARTED_AT),
    )

    report = await use_case.execute(Scope.PUBLIC)

    assert report.status is HealthStatus.OK
    assert report.scope is Scope.PUBLIC
    assert report.version == "1.0.0"
    assert report.uptime_seconds == 10
    assert report.checked_at == STARTED_AT + timedelta(seconds=10)


@pytest.mark.parametrize(
    ("statuses", "expected"),
    [
        ([HealthStatus.OK, HealthStatus.OK], HealthStatus.OK),
        ([HealthStatus.OK, HealthStatus.DEGRADED], HealthStatus.DEGRADED),
        ([HealthStatus.DEGRADED, HealthStatus.DOWN], HealthStatus.DOWN),
    ],
)
async def test_returns_worst_component_status(
    statuses: list[HealthStatus], expected: HealthStatus
) -> None:
    checks = [StubCheck(f"dep{i}", status) for i, status in enumerate(statuses)]
    use_case = GetHealthUseCase(
        clock=FakeClock(STARTED_AT),
        app_info=AppInfo(version="1.0.0", started_at=STARTED_AT),
        checks=checks,
    )

    report = await use_case.execute(Scope.ADMIN)

    assert report.status is expected
    assert [c.name for c in report.components] == [c.name for c in checks]
