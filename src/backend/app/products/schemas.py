from pydantic import BaseModel


class ProductBaseSchema(BaseModel):
    name: str
    description: str
    price: int
    quantity: int
    category_id: int


class ProductCreateSchema(ProductBaseSchema):
    pass


class ProductUpdateSchema(ProductBaseSchema):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    available: bool | None = None
    category_id: int | None = None


class ProductSchema(ProductBaseSchema):
    id: int
    available: bool
