from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_file_encoding="utf-8",
    )

    google_api_key: SecretStr | None = None
    datadog_api_key: SecretStr | None = None

    datadog_site: str = Field(
        default="https://http-intake.logs.us5.datadoghq.com/api/v2/logs"
    )


settings = Settings()
