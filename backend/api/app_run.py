from fastapi import FastAPI

from api.config import Settings
from api.container import build_container
from api.core.cors import configure_cors
from api.core.errors import register_error_handlers
from api.core.logs import configure_logging
from api.core.request_id import RequestIdMiddleware
from api.core.swagger import docs_urls
from api.routes.admin import admin_router
from api.routes.public import public_router
from api.routes.websocket import ws_router


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    configure_logging(settings.log_level)

    app = FastAPI(title="Bot Varejo API", version=settings.version, **docs_urls(settings))
    app.state.container = build_container(settings)

    configure_cors(app, settings)
    # Adicionado por último = mais externo: até o preflight do CORS recebe X-Request-ID.
    app.add_middleware(RequestIdMiddleware)

    app.include_router(public_router)
    app.include_router(admin_router)
    app.include_router(ws_router)
    register_error_handlers(app)
    return app
