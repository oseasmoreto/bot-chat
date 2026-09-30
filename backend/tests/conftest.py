from collections.abc import AsyncIterator, Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from api.app_run import create_app
from api.config import Settings

ALLOWED_ORIGIN = "http://localhost:3000"


@pytest.fixture
def settings() -> Settings:
    # _env_file=None: os testes não dependem do .env de quem roda.
    return Settings(_env_file=None, env="local", version="test", cors_origins=[ALLOWED_ORIGIN])


@pytest.fixture
def app(settings: Settings) -> FastAPI:
    return create_app(settings)


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
        yield http


@pytest.fixture
def ws_client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
