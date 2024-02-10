from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderProduct(SQLModel, table=True):
    order_id: int = Field(foreign_key="order.id", primary_key=True)
    product_id: int = Field(foreign_key="product.id", primary_key=True)
    quantity: int
    order: "Order" = Relationship(back_populates="products")
    product: "Product" = Relationship(back_populates="orders")
