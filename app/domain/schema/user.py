from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.domain.schema.validators.datetime import CustomDatetime
from app.domain.schema.validators.password import validate_password


class UserSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: str = EmailStr()
    password: str = Field(..., exclude=True)

    @field_validator("password", mode="before")
    @classmethod
    def pre_validate_password(cls, value: str) -> str:
        return validate_password(value=value)


class UserCreationResponse(UserSchema):
    id: UUID

    class Config:
        from_attributes = True
        json_encoders = {CustomDatetime: CustomDatetime.to_str}
