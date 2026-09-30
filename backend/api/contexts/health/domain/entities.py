from dataclasses import dataclass
from datetime import datetime

from api.contexts.health.domain.value_objects import HealthStatus
from api.core.scope import Scope


@dataclass(frozen=True, slots=True, kw_only=True)
class ComponentHealth:
    name: str
    status: HealthStatus
    detail: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class HealthReport:
    scope: Scope
    status: HealthStatus
    version: str
    uptime_seconds: float
    checked_at: datetime
    components: tuple[ComponentHealth, ...] = ()
