from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    SECRET_KEY: str = "secret_key"
    ALGORITHM: str = "HS256"


settings = Settings()  # type: ignore