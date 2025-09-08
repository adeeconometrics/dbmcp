from typing import List, Optional
from datetime import datetime
from enum import Enum as StrEnum
from sqlmodel import SQLModel, Field, Relationship


class BaseModel(SQLModel):
    """Base model for all database models."""
    created_at: datetime = Field(
        default_factory=datetime.now, nullable=False)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)


class Product(BaseModel, table=True):
    """SQLModel schema for products."""
    __tablename__ = "products"

    product_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    stock_quantity: int = Field(default=0)

    order_items: List["OrderItem"] = Relationship(back_populates="product")


class User(BaseModel, table=True):
    """SQLModel schema for users."""
    __tablename__ = "users"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)

    orders: List["Order"] = Relationship(back_populates="user")


class OrderStatus(StrEnum):
    """Enumeration for order status."""
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(BaseModel, table=True):
    """SQLModel schema for orders."""
    __tablename__ = "orders"

    order_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    order_date: datetime = Field(default_factory=datetime.now)
    status: str = Field(default=str(OrderStatus.PENDING))

    user: "User" = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(BaseModel, table=True):
    """SQLModel schema for order items."""
    __tablename__ = "order_items"

    order_id: int = Field(foreign_key="orders.order_id", primary_key=True)
    product_id: int = Field(
        foreign_key="products.product_id", primary_key=True)
    quantity: int = Field(default=1)

    order: "Order" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="order_items")
