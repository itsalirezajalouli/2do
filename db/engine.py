import os
from db.models import Plan, Task, CommandHistory  # noqa: F401

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()
engine = create_engine(f'sqlite:///{os.getenv("SQLITE_FILE_ADDR")}', echo=False)


def get_engine():
    return engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
