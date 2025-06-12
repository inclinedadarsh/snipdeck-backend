from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from src.models.snippet_versions import SnippetVersion


class Snippet(SQLModel, table=True):
    __tablename__ = "snippets"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    language: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    slug: str = Field(default=None, unique=True, index=True, nullable=False)
    versions: List["SnippetVersion"] = Relationship(back_populates="snippet")
