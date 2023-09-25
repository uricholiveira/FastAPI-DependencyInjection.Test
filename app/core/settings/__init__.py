from pydantic_settings import BaseSettings

from app.core.settings.app import ApplicationConfig
from app.core.settings.database import DatabaseConfig
from app.core.settings.util import UtilConfig


class Settings(BaseSettings):
    app: ApplicationConfig = ApplicationConfig()
    db: DatabaseConfig = DatabaseConfig()
    util: UtilConfig = UtilConfig()


settings = Settings()
