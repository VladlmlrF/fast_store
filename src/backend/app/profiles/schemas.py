from pydantic import BaseModel


class ProfileBaseSchema(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    phone_number: str


class ProfileCreateSchema(ProfileBaseSchema):
    pass


class ProfileUpdateSchema(ProfileBaseSchema):
    user_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None


class ProfileSchema(ProfileBaseSchema):
    id: int
