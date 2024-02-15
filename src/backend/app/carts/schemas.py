from pydantic import BaseModel


class CartBaseSchema(BaseModel):
    user_id: int


class CartCreateSchema(CartBaseSchema):
    pass


class CartSchema(CartBaseSchema):
    id: int
