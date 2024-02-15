from pydantic import BaseModel


class AddressBaseSchema(BaseModel):
    profile_id: int
    street: str
    city: str
    state: str
    postal_code: int
    country: str


class AddressCreateSchema(AddressBaseSchema):
    pass


class AddressUpdateSchema(AddressBaseSchema):
    profile_id: int | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: int | None = None
    country: str | None = None


class AddressSchema(AddressBaseSchema):
    id: int
