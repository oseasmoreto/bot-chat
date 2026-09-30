import pytest

from api.contexts.health.domain.value_objects import HealthStatus


def test_worst_returns_ok_when_there_are_no_statuses() -> None:
    assert HealthStatus.worst([]) is HealthStatus.OK


@pytest.mark.parametrize(
    ("statuses", "expected"),
    [
        ([HealthStatus.OK], HealthStatus.OK),
        ([HealthStatus.OK, HealthStatus.DEGRADED], HealthStatus.DEGRADED),
        ([HealthStatus.DOWN, HealthStatus.OK, HealthStatus.DEGRADED], HealthStatus.DOWN),
    ],
)
def test_worst_returns_most_severe_status(
    statuses: list[HealthStatus], expected: HealthStatus
) -> None:
    assert HealthStatus.worst(statuses) is expected
