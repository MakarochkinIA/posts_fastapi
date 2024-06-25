from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = 'CWA0JgyxaJ4VopXDnC3wsGAe5CWCSrPFHP8o29QEXis'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    USERS_OPEN_REGISTRATION: bool = True
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: str = '6379'
    PUSH_NOTIFICATIONS_CHANNEL: str = 'follow'

    # TODO: update type to EmailStr when sqlmodel supports it
    EMAIL_TEST_USER: str = "test@example.com"
    # TODO: update type to EmailStr when sqlmodel supports it
    FIRST_SUPERUSER: str = "admin@admin.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"


settings = Settings()
