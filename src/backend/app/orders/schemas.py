from pydantic import BaseModel


class OrderBaseSchema(BaseModel):
    user_id: int


class OrderCreateSchema(OrderBaseSchema):
    pass


class OrderUpdateSchema(BaseModel):
    coupon_id: int


class OrderSchema(OrderBaseSchema):
    id: int
    coupon_id: int | None = None
