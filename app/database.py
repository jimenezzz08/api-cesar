from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings

from .models import Base

USER = settings.DATABASE_USER
PASSWORD = settings.DATABASE_PASSWORD
HOST = settings.DATABASE_HOST
PORT = settings.DATABASE_PORT
DB_NAME = settings.DATABASE_NAME


SQL_ALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
