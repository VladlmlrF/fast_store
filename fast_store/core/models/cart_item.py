from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship

from .base import Base

if TYPE_CHECKING:
    from .cart import Cart
    from .product import Product


class CartItem(Base, table=True):
    cart_id: int = Field(foreign_key="cart.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    cart: "Cart" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="cart_items")
