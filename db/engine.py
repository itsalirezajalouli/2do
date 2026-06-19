import os
from db.models import Plan, Task, CommandHistory  # noqa: F401

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)


def get_engine():
    return engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
