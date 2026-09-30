from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

    env: Literal["local", "dev", "staging", "production"] = "local"
    version: str = "0.1.0"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    docs_enabled: bool = True
    # Origens do frontend autorizadas (CORS e handshake do WebSocket).
    # Via env, em JSON: APP_CORS_ORIGINS='["https://app.dominio.com.br"]'
    cors_origins: list[str] = ["http://localhost:3000"]
    # DynamoDB (docs/12-persistencia-dynamodb.md). Endpoint vazio = endpoint da AWS.
    aws_region: str = "sa-east-1"
    dynamodb_endpoint_url: str | None = None
    dynamodb_table_prefix: str = "bot-varejo-local"
