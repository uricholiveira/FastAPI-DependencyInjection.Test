from pydantic import BaseModel, EmailStr, Field, field_validator

from app.domain.schema.validators.password import validate_password


class LoginRequest(BaseModel):
    username: EmailStr
    password: str = Field(..., exclude=True)

    @field_validator("password", mode="before")
    @classmethod
    def pre_validate_password(cls, value: str) -> str:
        return validate_password(value=value)
