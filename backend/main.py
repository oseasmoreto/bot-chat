"""Ponto de entrada da aplicação.

- `python main.py` sobe o Uvicorn em `APP_HOST`:`APP_PORT` (padrão 0.0.0.0:8000).
- `uvicorn main:app` (ou outro servidor ASGI) usa o objeto `app`.
"""

import uvicorn

from api.app_run import create_app
from api.config import Settings

settings = Settings()
app = create_app(settings)


def run() -> None:
    # log_config=None: o Uvicorn mantém o log JSON configurado por create_app.
    # X-Forwarded-* só é aceito dos IPs em FORWARDED_ALLOW_IPS (lido pelo Uvicorn).
    uvicorn.run(app, host=settings.host, port=settings.port, proxy_headers=True, log_config=None)


if __name__ == "__main__":
    run()
