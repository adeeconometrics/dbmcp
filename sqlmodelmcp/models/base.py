from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    """Base model for all database models."""
    created_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)
