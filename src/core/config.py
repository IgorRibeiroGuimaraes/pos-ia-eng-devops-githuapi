from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Ambiente
    environment: str = Field(default="development")

    # Banco de Dados
    database_url: str = Field(default="postgresql://postgres:postgres@localhost:5432/github_pipeline")

    # GitHub API
    github_token: str = Field(default="")
    github_api_base_url: str = Field(default="https://api.github.com")

    # API
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    api_debug: bool = Field(default=False)

    # Prefect
    prefect_api_url: str = Field(default="http://localhost:4200/api")


settings = Settings()
