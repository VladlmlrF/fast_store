from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship

from .base import Base

if TYPE_CHECKING:
    from .profile import Profile


class Address(Base, table=True):
    profile_id: int = Field(foreign_key="profile.id")
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    user: "Profile" = Relationship(back_populates="addresses")
