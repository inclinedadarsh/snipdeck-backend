from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv, find_dotenv
import os
from src.models.snippets import Snippet  # noqa: F401
from src.models.snippet_versions import SnippetVersion  # noqa: F401

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
