from typing import Annotated

from fastapi import Depends

from api.container import Container, get_container
from api.contexts.health.application.get_health import GetHealthUseCase


def get_health_use_case(
    container: Annotated[Container, Depends(get_container)],
) -> GetHealthUseCase:
    return container.get_health
