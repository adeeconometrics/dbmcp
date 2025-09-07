from sqlmodel import Field, Relationship
from typing import Optional, List
from models.base import BaseModel
from uuid import uuid4


class Product(BaseModel, table=True):
    __tablename__ = "products"

    product_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    stock_quantity: int = Field(default=0)

    order_items: List["OrderItem"] = Relationship(back_populates="product")
