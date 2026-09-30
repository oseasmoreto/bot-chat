from fastapi import APIRouter

from api.contexts.health.presentation.http import build_health_router
from api.core.scope import Scope

public_router = APIRouter(prefix="/api/v1/public", tags=["public"])
public_router.include_router(build_health_router(Scope.PUBLIC))
