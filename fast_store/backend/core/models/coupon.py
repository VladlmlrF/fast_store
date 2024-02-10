from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship

from .base import Base

if TYPE_CHECKING:
    from .order import Order


class Coupon(Base, table=True):
    code: str = Field(index=True)
    discount: int
    valid_from: datetime
    valid_until: datetime
    orders: list["Order"] = Relationship(back_populates="coupon")
