from pydantic import Field
from pydantic_settings import BaseSettings


class LogConfig(BaseSettings):
    level: str = Field("INFO", env="LOG_LEVEL")


class UtilConfig(BaseSettings):
    log: LogConfig = LogConfig()
