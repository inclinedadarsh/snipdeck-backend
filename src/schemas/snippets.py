from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    pass


class SnippetCreate(BaseModel):
    title: str
    description: Optional[str] = None
    language: str
    content: str
    commit_message: str


class SnippetVersionRead(BaseModel):
    id: int
    content: str
    commit_message: str
    version_number: int
    created_at: datetime
    updated_at: datetime


class SnippetRead(BaseModel):
    id: int
    slug: str
    title: str
    description: Optional[str] = None
    language: str
    created_at: datetime
    updated_at: datetime
    versions: List[SnippetVersionRead]


class SnippetVersionWithSnippetRead(BaseModel):
    id: int
    content: str
    commit_message: str
    version_number: int
    created_at: datetime
    updated_at: datetime
    snippet_id: int
    title: str
    description: Optional[str] = None
    language: str
