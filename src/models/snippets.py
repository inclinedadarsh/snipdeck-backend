from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from src.models.snippet_versions import SnippetVersion


class SnippetBase(SQLModel):
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    language: str = Field(nullable=False)


class Snippet(SnippetBase, table=True):
    __tablename__ = "snippets"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    slug: str = Field(default=None, unique=True, index=True)
    versions: List["SnippetVersion"] = Relationship(back_populates="snippet")


class SnippetCreate(SnippetBase):
    pass


class SnippetRead(SnippetBase):
    id: int
    created_at: datetime
    updated_at: datetime
    slug: str
    versions: List["SnippetVersion"]
