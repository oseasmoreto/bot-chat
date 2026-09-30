from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from api.contexts.health.application.get_health import GetHealthUseCase
from api.contexts.health.domain.value_objects import HealthStatus
from api.contexts.health.presentation.dependencies import get_health_use_case
from api.contexts.health.presentation.schemas import HealthResponse
from api.core.scope import Scope


def build_health_router(scope: Scope) -> APIRouter:
    router = APIRouter(prefix="/health", tags=["health"])

    @router.get(
        "",
        summary=f"Health check do escopo {scope.value}",
        operation_id=f"get{scope.value.capitalize()}Health",
        responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": HealthResponse}},
    )
    async def get_health(
        response: Response,
        use_case: Annotated[GetHealthUseCase, Depends(get_health_use_case)],
    ) -> HealthResponse:
        report = await use_case.execute(scope)
        if report.status is HealthStatus.DOWN:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthResponse.from_domain(report)

    return router
