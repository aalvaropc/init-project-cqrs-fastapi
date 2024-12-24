from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

# Base para tus modelos
Base = declarative_base()

# Base de datos de ESCRITURA (Primary)
engine_writer = create_engine(settings.WRITER_DATABASE_URL, echo=False, future=True)
SessionLocalWriter = sessionmaker(bind=engine_writer, autoflush=False, autocommit=False, future=True)

# Base de datos de LECTURA (Replica)
engine_reader = create_engine(settings.READER_DATABASE_URL, echo=False, future=True)
SessionLocalReader = sessionmaker(bind=engine_reader, autoflush=False, autocommit=False, future=True)
