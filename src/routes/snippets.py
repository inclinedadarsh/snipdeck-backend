from fastapi import APIRouter
from sqlmodel import Session
from src.schemas.snippets import SnippetCreate, SnippetRead, SnippetVersionRead
from src.models.snippets import Snippet
from src.models.snippet_versions import SnippetVersion
from src.db import engine
from src.services.snippets import create_slug

router = APIRouter()


@router.post("/", response_model=SnippetRead)
def create_snippet(snippet_data: SnippetCreate):
    with Session(engine) as session:
        slug = create_slug()

        snippet_version = SnippetVersion(
            content=snippet_data.content,
            commit_message="Initial commit",
            version_number=1,
        )

        snippet = Snippet(
            title=snippet_data.title,
            description=snippet_data.description,
            language=snippet_data.language,
            versions=[snippet_version],
            slug=slug,
        )

        session.add(snippet)
        session.commit()
        session.refresh(snippet)
        session.refresh(snippet_version)

        snippet_version_read = SnippetVersionRead(
            id=snippet_version.id,
            content=snippet_version.content,
            commit_message=snippet_version.commit_message,
            version_number=snippet_version.version_number,
            created_at=snippet_version.created_at,
            updated_at=snippet_version.updated_at,
        )

        snippet_read = SnippetRead(
            id=snippet.id,
            slug=snippet.slug,
            title=snippet.title,
            description=snippet.description,
            language=snippet.language,
            created_at=snippet.created_at,
            updated_at=snippet.updated_at,
            versions=[snippet_version_read],
        )

    return snippet_read
