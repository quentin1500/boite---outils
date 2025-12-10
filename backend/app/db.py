from sqlmodel import create_engine, Session
from sqlmodel import SQLModel
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tools.db")
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
