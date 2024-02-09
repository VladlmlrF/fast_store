from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship

from .base import Base

if TYPE_CHECKING:
    from .product import Product


class Category(Base, table=True):
    name: str = Field(index=True)
    products: list["Product"] = Relationship(back_populates="category")
