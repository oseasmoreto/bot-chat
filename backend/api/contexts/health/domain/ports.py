from datetime import datetime
from typing import Protocol

from api.contexts.health.domain.entities import ComponentHealth


class ClockPort(Protocol):
    def now(self) -> datetime: ...


class HealthCheckPort(Protocol):
    """Verificação de uma dependência (ex.: DynamoDB, API de parceiro)."""

    @property
    def name(self) -> str: ...

    async def check(self) -> ComponentHealth: ...
