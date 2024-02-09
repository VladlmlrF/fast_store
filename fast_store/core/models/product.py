from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship

from .base import Base

if TYPE_CHECKING:
    from .category import Category
    from .review import Review
    from .cart import CartItem


class Product(Base, table=True):
    name: str = Field(index=True)
    description: str
    price: int = Field(index=True)
    quantity: int
    available: bool = Field(default=True)
    category_id: int = Field(foreign_key="category.id")
    category: "Category" = Relationship(back_populates="products")
    reviews: list["Review"] = Relationship(back_populates="product")
    cart_items: list["CartItem"] = Relationship(back_populates="product")
