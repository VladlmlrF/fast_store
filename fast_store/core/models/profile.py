from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .address import Address


class Profile(Base, table=True):
    user_id: int = Field(foreign_key="user.id")
    first_name: str
    last_name: str
    phone_number: str | None = None
    user: "User" = Relationship(back_populates="profile")
    addresses: list["Address"] = Relationship(back_populates="profile")
