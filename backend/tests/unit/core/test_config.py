import pytest

from api.config import Settings


def test_reads_app_prefixed_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "staging")
    monkeypatch.setenv("APP_DOCS_ENABLED", "false")
    monkeypatch.setenv("APP_CORS_ORIGINS", '["https://app.example.com"]')

    settings = Settings(_env_file=None)

    assert settings.env == "staging"
    assert settings.docs_enabled is False
    assert settings.cors_origins == ["https://app.example.com"]


def test_dynamodb_endpoint_defaults_to_aws(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("APP_DYNAMODB_ENDPOINT_URL", raising=False)

    assert Settings(_env_file=None).dynamodb_endpoint_url is None
