from pydantic import BaseModel


class CartItemBaseSchema(BaseModel):
    cart_id: int
    product_id: int
    quantity: int


class CartItemCreateSchema(CartItemBaseSchema):
    pass


class CartItemUpdateSchema(CartItemBaseSchema):
    cart_id: int | None = None
    product_id: int | None = None
    quantity: int | None = None


class CartItemSchema(CartItemBaseSchema):
    id: int
