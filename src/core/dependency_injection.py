from typing import Generator
from src.core.db import SessionLocalWriter, SessionLocalReader


def get_db_writer() -> Generator:
    """
    Dependency injection for the write database session.
    """
    db = SessionLocalWriter()
    try:
        yield db
    finally:
        db.close()


def get_db_reader() -> Generator:
    """
    Dependency injection for the read database session.
    """
    db = SessionLocalReader()
    try:
        yield db
    finally:
        db.close()