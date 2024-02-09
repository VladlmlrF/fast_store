from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .coupon import Coupon
    from .order_product import OrderProduct


class Order(Base, table=True):
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="orders")
    products: list["OrderProduct"] = Relationship(back_populates="order")
    coupon_id: int | None = Field(default=None, foreign_key="coupon.id")
    coupon: "Coupon | None" = Relationship(back_populates="orders")
