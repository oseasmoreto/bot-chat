import asyncio
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

from api.contexts.health.domain.entities import HealthReport
from api.contexts.health.domain.ports import ClockPort, HealthCheckPort
from api.contexts.health.domain.value_objects import HealthStatus
from api.core.scope import Scope


@dataclass(frozen=True, slots=True)
class AppInfo:
    version: str
    started_at: datetime


class GetHealthUseCase:
    def __init__(
        self,
        *,
        clock: ClockPort,
        app_info: AppInfo,
        checks: Sequence[HealthCheckPort] = (),
    ) -> None:
        self._clock = clock
        self._app_info = app_info
        self._checks = tuple(checks)

    async def execute(self, scope: Scope) -> HealthReport:
        components = tuple(await asyncio.gather(*(c.check() for c in self._checks)))
        now = self._clock.now()
        return HealthReport(
            scope=scope,
            status=HealthStatus.worst(c.status for c in components),
            version=self._app_info.version,
            uptime_seconds=(now - self._app_info.started_at).total_seconds(),
            checked_at=now,
            components=components,
        )
