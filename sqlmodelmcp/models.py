from typing import List, Optional
from datetime import datetime
from enum import Enum as StrEnum
from uuid import uuid4
from sqlmodel import SQLModel, Field, Relationship


class BaseModel(SQLModel):
    """Base model for all database models."""
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)


class Category(BaseModel, table=True):
    """SQLModel schema for product categories."""
    __tablename__ = "categories"

    category_id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    description: Optional[str] = None

    products: List["Product"] = Relationship(back_populates="category")


class Product(BaseModel, table=True):
    """SQLModel schema for products."""
    __tablename__ = "products"

    product_id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    price: float
    stock_quantity: int = Field(default=0)
    category_id: str = Field(foreign_key="categories.category_id")
    category: Optional["Category"] = Relationship(back_populates="products")

    order_items: List["OrderItem"] = Relationship(back_populates="product")


class Address(BaseModel, table=True):
    """SQLModel schema for addresses."""
    __tablename__ = "addresses"

    address_id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True)

    street: str
    city: str
    state: Optional[str] = None
    zip_code: str
    country: str

    users: List["User"] = Relationship(back_populates="address")


class User(BaseModel, table=True):
    """SQLModel schema for users."""
    __tablename__ = "users"

    user_id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True)
    address_id: Optional[str] = Field(
        default=None, foreign_key="addresses.address_id")

    firstname: str
    lastname: str
    password: str
    phone: Optional[str] = None
    payment_info: Optional[str] = None
    email: str = Field(index=True, unique=True)

    address: Optional[Address] = Relationship(back_populates="users")
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

    order_id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.user_id")
    order_date: datetime = Field(default_factory=datetime.now)
    status: str = Field(default=str(OrderStatus.PENDING))

    user: "User" = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(BaseModel, table=True):
    """SQLModel schema for order items."""
    __tablename__ = "order_items"

    order_id: str = Field(foreign_key="orders.order_id", primary_key=True)
    product_id: str = Field(
        foreign_key="products.product_id", primary_key=True)
    quantity: int = Field(default=1)

    order: "Order" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="order_items")
