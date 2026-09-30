import dataclasses

import pytest

from api.contexts.health.domain.entities import ComponentHealth, HealthReport
from api.contexts.health.domain.value_objects import HealthStatus
from api.core.scope import Scope
from tests.fakes import STARTED_AT


def test_report_has_no_components_by_default() -> None:
    report = HealthReport(
        scope=Scope.PUBLIC,
        status=HealthStatus.OK,
        version="1.0.0",
        uptime_seconds=0,
        checked_at=STARTED_AT,
    )

    assert report.components == ()


def test_component_is_immutable() -> None:
    component = ComponentHealth(name="database", status=HealthStatus.OK)

    with pytest.raises(dataclasses.FrozenInstanceError):
        component.status = HealthStatus.DOWN  # type: ignore[misc]  # testa o frozen
