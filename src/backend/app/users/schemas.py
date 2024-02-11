from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import field_validator

from src.backend.app.core.models.user import Role


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 4:
            raise ValueError("Username must be at least 4 characters long")
        return value


class UserCreateSchema(UserBaseSchema):
    password: str


class UserUpdateSchema(UserBaseSchema):
    username: str | None = None
    email: EmailStr | None = None


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool
    role: Role

    model_config = ConfigDict(from_attributes=True)
