# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from src.apps.users.infrastructure.orm_models import Base

# @pytest.fixture(scope="session")
# def test_db_engine():
#     engine = create_engine("sqlite:///:memory:", echo=False, future=True)
#     Base.metadata.create_all(bind=engine)
#     return engine

# @pytest.fixture(scope="function")
# def test_db_session(test_db_engine):
#     SessionTest = sessionmaker(bind=test_db_engine, autoflush=False, autocommit=False, future=True)
#     session = SessionTest()
#     try:
#         yield session
#     finally:
#         session.close()

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.apps.users.infrastructure.orm_models import Base

@pytest.fixture(scope="session")
def test_db_engine():
    # Para pruebas, podemos usar SQLite en memoria.
    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    SessionTest = sessionmaker(bind=test_db_engine, autoflush=False, autocommit=False, future=True)
    session = SessionTest()
    try:
        yield session
    finally:
        session.close()
