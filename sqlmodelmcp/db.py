from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

DATABASE_URL = "sqlite:///../demo.sqlite"  # swap with Postgres/MySQL if needed
engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    """Create all tables in the database."""
    from models import user, product, order, order_item  # ensure models are imported
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Yield a database session (dependency-friendly)."""
    with Session(engine) as session:
        yield session
