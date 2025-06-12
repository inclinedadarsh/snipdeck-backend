from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from src.models.snippets import Snippet


class SnippetVersionBase(SQLModel):
    content: str = Field(nullable=False)
    commit_message: str = Field(nullable=False)


class SnippetVersion(SnippetVersionBase, table=True):
    __tablename__ = "snippet_versions"
    id: Optional[int] = Field(default=None, primary_key=True)
    version_number: int = Field(nullable=False)
    snippet_id: int = Field(nullable=False, foreign_key="snippets.id")
    snippet: Snippet = Relationship(back_populates="versions")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class SnippetVersionCreate(SnippetVersionBase):
    snippet_id: int = Field(nullable=False)


class SnippetVersionRead(SnippetVersionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    version_number: int
