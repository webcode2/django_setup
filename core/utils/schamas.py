from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, validator, field_validator


class UserBaseSchema(BaseModel):
    first_name: str = Field(min_length=2, max_length=50, default="", pattern=r"^[a-zA-Z]+$")
    last_name: str = Field(min_length=2, max_length=50, default="", pattern=r"^[a-zA-Z]+$")
    email: EmailStr = Field()


class UserCreateSchema(UserBaseSchema):
    password: str = Field(min_length=6, max_length=100)

    @field_validator('first_name', "last_name")
    @classmethod
    def name_must_be_alphabetic(cls, value):
        if not value.isalpha():
            raise ValueError(f"{value} must contain only alphabets")
        return value


class UserReadSchema(UserBaseSchema):
    is_superuser: bool
    is_active: bool
    last_login: datetime
    date_joined:datetime
