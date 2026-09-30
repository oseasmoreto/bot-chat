"""Dublês que implementam as ports (Protocol) do domínio."""

from datetime import UTC, datetime

from api.contexts.health.domain.entities import ComponentHealth
from api.contexts.health.domain.value_objects import HealthStatus

STARTED_AT = datetime(2026, 1, 1, tzinfo=UTC)


class FakeClock:
    def __init__(self, now: datetime) -> None:
        self._now = now

    def now(self) -> datetime:
        return self._now


class StubCheck:
    def __init__(self, name: str, status: HealthStatus) -> None:
        self.name = name
        self._status = status

    async def check(self) -> ComponentHealth:
        return ComponentHealth(name=self.name, status=self._status)
