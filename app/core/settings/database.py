from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseParamsConfig(BaseSettings):
    auto_commit: bool = True
    auto_flush: bool = True
    check_same_thread: bool = False


class DatabaseConnConfig(BaseSettings):
    driver: str = Field("postgresql", env="DB_DRIVER")
    user: str = Field("postgres", env="DB_USER")
    password: str = Field("supersecretpassword", env="DB_PASSWORD")
    host: str = Field("localhost", env="DB_HOST")
    port: int = Field(5432, env="DB_PORT")
    name: str = Field("postgres", env="DB_NAME")


class DatabaseConfig(BaseSettings):
    params: DatabaseParamsConfig = DatabaseParamsConfig()
    connection: DatabaseConnConfig = DatabaseConnConfig()
    url: str = f"{connection.driver}://{connection.user}:{connection.password}@{connection.host}:{connection.port}/{connection.name}"
