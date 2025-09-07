from sqlmodel import Field, Relationship
from typing import Optional, List
from models.base import BaseModel
from uuid import uuid4


class User(BaseModel, table=True):
    __tablename__ = "users"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)

    # relationships
    orders: List["Order"] = Relationship(back_populates="user")
