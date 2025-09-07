from sqlmodel import Field, Relationship
from typing import Optional, List
from datetime import datetime
from models.base import BaseModel
from uuid import uuid4


class OrderStatus(str):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(BaseModel, table=True):
    __tablename__ = "orders"

    order_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    order_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default=OrderStatus.PENDING)

    # relationships
    user: "User" = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")
