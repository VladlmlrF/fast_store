from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship

from .base import Base

if TYPE_CHECKING:
    from .order import Order
    from .cart import Cart
    from .profile import Profile


class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class User(Base, table=True):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    role: Role = Field(default=Role.USER)
    orders: list["Order"] = Relationship(back_populates="user")
    cart: "Cart" = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )
    profile: "Profile" = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )
