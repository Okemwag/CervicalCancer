from typing import Generator
from sqlalchemy.orm import Session
from .connection import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that yields database sessions.
    Used with FastAPI's Depends() to inject database sessions into routes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session() -> Session:
    """
    Get a database session directly (useful for scripts/services).
    Remember to close the session when done!
    """
    return SessionLocal()
