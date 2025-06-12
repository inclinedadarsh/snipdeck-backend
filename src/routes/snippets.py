from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from src.schemas.snippets import (
    SnippetCreate,
    SnippetRead,
    SnippetVersionCreate,
    SnippetVersionRead,
    SnippetVersionWithSnippetRead,
)
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
            commit_message=snippet_data.commit_message,
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


@router.get("/{slug}", response_model=SnippetRead)
def get_snippet(slug: str):
    with Session(engine) as session:
        snippet = session.exec(select(Snippet).where(Snippet.slug == slug)).first()

        if not snippet:
            raise HTTPException(status_code=404, detail="Snippet not found")

        snippet_read = SnippetRead(
            id=snippet.id,
            slug=snippet.slug,
            title=snippet.title,
            description=snippet.description,
            language=snippet.language,
            created_at=snippet.created_at,
            updated_at=snippet.updated_at,
            versions=[
                SnippetVersionRead(
                    id=version.id,
                    content=version.content,
                    commit_message=version.commit_message,
                    version_number=version.version_number,
                    created_at=version.created_at,
                    updated_at=version.updated_at,
                )
                for version in snippet.versions
            ],
        )

        return snippet_read


@router.post("/{slug}/versions", response_model=SnippetVersionWithSnippetRead)
def create_snippet_version(slug: str, version_data: SnippetVersionCreate):
    with Session(engine) as session:
        snippet = session.exec(select(Snippet).where(Snippet.slug == slug)).first()
        if not snippet:
            raise HTTPException(status_code=404, detail="Snippet not found")

        version = SnippetVersion(
            content=version_data.content,
            commit_message=version_data.commit_message,
            version_number=snippet.versions[-1].version_number + 1,
        )

        snippet.versions.append(version)
        session.add(snippet)
        session.commit()
        session.refresh(snippet)
        session.refresh(version)

        return SnippetVersionWithSnippetRead(
            id=version.id,
            content=version.content,
            commit_message=version.commit_message,
            version_number=version.version_number,
            created_at=version.created_at,
            updated_at=version.updated_at,
            title=snippet.title,
            description=snippet.description,
            language=snippet.language,
            snippet_id=snippet.id,
        )


@router.get(
    "/{slug}/versions/{version_number}", response_model=SnippetVersionWithSnippetRead
)
def get_snippet_version(slug: str, version_number: int):
    with Session(engine) as session:
        snippet = session.exec(select(Snippet).where(Snippet.slug == slug)).first()
        if not snippet:
            raise HTTPException(status_code=404, detail="Snippet not found")

        version = session.exec(
            select(SnippetVersion).where(
                SnippetVersion.snippet_id == snippet.id,
                SnippetVersion.version_number == version_number,
            )
        ).first()

        if not version:
            raise HTTPException(status_code=404, detail="Version not found")

        return SnippetVersionWithSnippetRead(
            id=version.id,
            content=version.content,
            commit_message=version.commit_message,
            version_number=version.version_number,
            created_at=version.created_at,
            updated_at=version.updated_at,
            snippet_id=snippet.id,
            title=snippet.title,
            description=snippet.description,
            language=snippet.language,
        )
