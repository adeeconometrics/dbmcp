from sqlmodel import Field, Relationship
from models.base import BaseModel


class OrderItem(BaseModel, table=True):
    __tablename__ = "order_items"

    order_id: int = Field(foreign_key="orders.order_id", primary_key=True)
    product_id: int = Field(
        foreign_key="products.product_id", primary_key=True)
    quantity: int = Field(default=1)

    order: "Order" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="order_items")
