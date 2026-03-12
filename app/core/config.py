from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Deribit Price Service"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "deribit_db"
    postgres_host: str = "db"
    postgres_port: int = 5432

    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/deribit_db"

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_url: str = "redis://redis:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()