from fastapi import APIRouter

from api.contexts.health.presentation.http import build_health_router
from api.core.scope import Scope

# Futuro: dependencies=[Depends(require_admin)] quando o context identity existir.
admin_router = APIRouter(prefix="/api/v1/admin", tags=["admin"])
admin_router.include_router(build_health_router(Scope.ADMIN))
