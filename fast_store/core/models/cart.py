from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .cart_item import CartItem


class Cart(Base, table=True):
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="cart")
    items: list["CartItem"] = Relationship(back_populates="cart")
