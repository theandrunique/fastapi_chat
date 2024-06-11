from pydantic import MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
        env_prefix="MONGO_",
    )
    DATABASE_NAME: str = "items"
    URI: MongoDsn


class SecuritySettings(BaseSettings):
    AUTHORIZATION_SERVER_URL: str
    CLIENT_ID: str
    ALGORITHM: str = "RS256"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    PROJECT_NAME: str = "FastAPI Chat"
    SERVER_HOST: str = "http://localhost"

    KAFKA_BROKER_URL: str

    SECURITY: SecuritySettings = SecuritySettings() # type: ignore

    MONGO: MongoSettings = MongoSettings()  # type: ignore


settings = Settings()  # type: ignore
