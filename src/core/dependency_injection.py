from typing import Generator
from src.core.db import SessionLocalWriter, SessionLocalReader

def get_db_writer() -> Generator:
    db = SessionLocalWriter()
    try:
        yield db
    finally:
        db.close()

def get_db_reader() -> Generator:
    db = SessionLocalReader()
    try:
        yield db
    finally:
        db.close()
