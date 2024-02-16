from pydantic import BaseModel


class OrderProductBaseSchema(BaseModel):
    order_id: int
    product_id: int
    quantity: int


class OrderProductCreateSchema(OrderProductBaseSchema):
    pass


class OrderProductUpdateSchema(BaseModel):
    quantity: int | None = None


class OrderProductSchema(OrderProductBaseSchema):
    pass
