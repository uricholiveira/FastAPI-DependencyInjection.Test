from pydantic_settings import BaseSettings


class ApplicationSecurityConfig(BaseSettings):
    algorithm: str = "HS256"
    secret_key: str = "3b31ae44218409d2a080ae104d7ded390d8a898ba3f327e4a0161e1624f562a6"
    access_token_expire_minutes: int = 15


class ApplicationConfig(BaseSettings):
    title: str = "Backend"
    version: str = "0.1.0"
    description: str = "A simple backend api template"
    host: str = "localhost"
    port: int = 3000
    security: ApplicationSecurityConfig = ApplicationSecurityConfig()
