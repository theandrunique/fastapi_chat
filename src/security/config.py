from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    AUTHORIZATION_SERVER_URL: str = "http://theandru.ru:8000"
    CLIENT_ID: str = "5353554b-557e-4872-976e-baf669b2c708"
    ALGORITHM: str = "RS256"


settings = Settings()  # type: ignore