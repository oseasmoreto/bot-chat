from typing import TypedDict

from api.config import Settings


class DocsUrls(TypedDict):
    docs_url: str | None
    redoc_url: str | None
    openapi_url: str | None


def docs_urls(settings: Settings) -> DocsUrls:
    """URLs do Swagger, ReDoc e OpenAPI. `APP_DOCS_ENABLED=false` desliga as três."""
    if not settings.docs_enabled:
        return DocsUrls(docs_url=None, redoc_url=None, openapi_url=None)
    return DocsUrls(docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json")
