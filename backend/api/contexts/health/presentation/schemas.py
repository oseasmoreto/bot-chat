from datetime import datetime
from typing import Self

from api.contexts.health.domain.entities import HealthReport
from api.contexts.health.domain.value_objects import HealthStatus
from api.core.schemas import BaseSchema
from api.core.scope import Scope


class ComponentHealthResponse(BaseSchema):
    name: str
    status: HealthStatus
    detail: str | None = None


class HealthResponse(BaseSchema):
    status: HealthStatus
    scope: Scope
    version: str
    uptime_seconds: float
    checked_at: datetime
    components: list[ComponentHealthResponse]

    @classmethod
    def from_domain(cls, report: HealthReport) -> Self:
        return cls(
            status=report.status,
            scope=report.scope,
            version=report.version,
            uptime_seconds=report.uptime_seconds,
            checked_at=report.checked_at,
            components=[
                ComponentHealthResponse(name=c.name, status=c.status, detail=c.detail)
                for c in report.components
            ],
        )
