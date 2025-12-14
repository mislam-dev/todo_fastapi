import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


CURRENT_FILE_DIR = Path(__file__).resolve().parent

# 2. Go up two levels to find the project root
# Result: .../todo-fastapi
PROJECT_ROOT = CURRENT_FILE_DIR.parent.parent

# 3. Join with the .env filename
ENV_PATH = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()  # type: ignore
