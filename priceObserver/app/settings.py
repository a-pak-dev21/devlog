from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import SecretStr



BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_host: str = "db"
    postgres_db: str = "price_observer"
    postgres_port: int = 5432
    
    log_level: str = "DEBUG"

    admin_username: str
    admin_password_hash: SecretStr
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int | None


    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
        case_sensitive=False
    )

    @property
    def database_url(self) -> str:
        return(
            f"postgresql+psycopg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings() #type: ignore[call-arg]