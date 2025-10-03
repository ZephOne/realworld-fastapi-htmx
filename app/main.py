from fastapi import FastAPI

from app.routers.articles import router as articles_router
from app.routers.tags import router as tags_router
from app.routers.users import router as users_router


app = FastAPI()

app.include_router(articles_router)
app.include_router(tags_router)
app.include_router(users_router)
