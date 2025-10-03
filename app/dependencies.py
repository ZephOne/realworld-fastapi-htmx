from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.db import get_session

DbSessionDep = Annotated[Session, Depends(get_session)]
