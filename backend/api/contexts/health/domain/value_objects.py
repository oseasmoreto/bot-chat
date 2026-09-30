from collections.abc import Iterable
from enum import StrEnum
from typing import Final


class HealthStatus(StrEnum):
    OK = "ok"
    DEGRADED = "degraded"
    DOWN = "down"

    @classmethod
    def worst(cls, statuses: Iterable["HealthStatus"]) -> "HealthStatus":
        """Status agregado = o pior entre os componentes. Sem componentes → OK."""
        return max(statuses, key=_SEVERITY.__getitem__, default=cls.OK)


_SEVERITY: Final[dict[HealthStatus, int]] = {
    HealthStatus.OK: 0,
    HealthStatus.DEGRADED: 1,
    HealthStatus.DOWN: 2,
}
