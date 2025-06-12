from sqlmodel import Session, select
from src.db import engine
from src.models.snippets import Snippet
import random
import string


def create_slug() -> str:
    with Session(engine) as session:
        for _ in range(10):
            slug = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))

            statement = select(Snippet).where(Snippet.slug == slug)
            result = session.exec(statement).first()
            if not result:
                return slug

        raise ValueError("Could not generate unique slug after 10 attempts")
