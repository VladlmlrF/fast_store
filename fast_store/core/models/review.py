from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship

from .base import Base

if TYPE_CHECKING:
    from .product import Product


class Rating(str, Enum):
    ONE = "ONE"
    TWO = "TWO"
    THREE = "THREE"
    FOUR = "FOUR"
    FIVE = "FIVE"


class Review(Base, table=True):
    product_id: int = Field(foreign_key="product.id")
    product: "Product" = Relationship(back_populates="reviews")
    review_text: str
    rating: Rating = Field(index=True)
