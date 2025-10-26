"""Configuration management"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # API
    api_title: str = "Apology-as-a-Service API"
    api_version: str = "1.0.0"
    api_description: str = "LLM-powered apology generation platform"

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"

    # Database
    database_url: str = "postgresql://sorry:password@localhost:5432/sorrydb"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Rate Limiting
    rate_limit_anon: int = 10
    rate_limit_authed: int = 100

    # Auth
    nextauth_secret: str = "dev-secret-change-in-production"
    nextauth_url: str = "https://sorry.monster"
    google_client_id: str = ""
    google_client_secret: str = ""

    # Observability
    sentry_dsn: str = ""
    otel_exporter_otlp_endpoint: str = ""

    # Environment
    environment: str = "production"


settings = Settings()
