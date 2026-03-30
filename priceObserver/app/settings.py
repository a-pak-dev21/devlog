from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    user: str = "postgres"
    password: str = "password"
    host: str = "db"
    db: str = "price_observer"
    port: int = 5432


    log_level: str = "DEBUG"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_prefix="POSTGRES_",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return(
            f"postgresql+psycopg://{self.user}:"
            f"{self.password}@{self.host}:"
            f"{self.port}/{self.db}"
        )


settings = Settings()