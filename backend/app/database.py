# backend/app/database.py
# DB connection (SQLite + Phase 2 ready for other DBs)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from contextlib import contextmanager

from .config import settings

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass

# Common engine creation logic
connect_args = {}
if str(settings.DATABASE_URL).startswith("sqlite"):
    # Needed for SQLite in FastAPI multi-threaded mode
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    FastAPI dependency for DB sessions.
    Works for both Phase 1 (SQLite) and Phase 2 (PostgreSQL/MySQL).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def db_session():
    """
    Context manager for scripts / non-FastAPI usage.
    Example:
        with db_session() as db:
            db.query(MyModel).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
