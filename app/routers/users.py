from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.dependencies import DbSessionDep
from app.models import User

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


@router.get("/api/users")
async def read_users(db_session: DbSessionDep):
    users = db_session.exec(select(User)).all()
    return users


@router.get("/api/user/{username}")
async def read_user(username: str, db_session: DbSessionDep):
    user = db_session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
