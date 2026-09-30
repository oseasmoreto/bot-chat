from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import Settings
from api.core.request_id import REQUEST_ID_HEADER


def configure_cors(app: FastAPI, settings: Settings) -> None:
    """Front e API em domínios diferentes → CORS explícito, só para origens conhecidas.

    A mesma lista (`APP_CORS_ORIGINS`) valida o Origin do WebSocket (routes/websocket.py).
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=[REQUEST_ID_HEADER],
    )
