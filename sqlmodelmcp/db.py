from typing import Generator, Final
from sqlmodel import SQLModel, create_engine, Session

# swap with Postgres/MySQL if needed
DATABASE_URL: Final[str] = "sqlite:///../demo.sqlite"
engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    """Create all tables in the database."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Yield a database session (dependency-friendly)."""
    with Session(engine) as session:
        yield session
