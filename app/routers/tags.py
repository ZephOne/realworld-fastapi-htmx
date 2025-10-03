from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.dependencies import DbSessionDep
from app.models import Tag


router = APIRouter()


@router.get("/api/tags")
async def read_tags(db_session: DbSessionDep):
    tags = db_session.exec(select(Tag)).all()
    return tags


@router.get("/api/tag/{tag_id}")
async def read_tag(tag_id: int, db_session: DbSessionDep):
    tag = db_session.exec(select(Tag).where(Tag.id == tag_id)).first()
    if not tag:
        raise HTTPException(status_code=404, detail="tag not found")
    return tag
