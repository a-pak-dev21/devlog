from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:password@localhost:5431/price_observer"
    log_level: str = "DEBUG"
    model_config = SettingsConfigDict(env_file= BASE_DIR / ".env")


settings = Settings()