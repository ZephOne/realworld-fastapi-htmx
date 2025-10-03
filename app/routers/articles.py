from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import aliased
from sqlmodel import select

from app.dependencies import DbSessionDep
from app.models import Article, ArticlesHaveTags, Tag, User, UsersFavourArticles


router = APIRouter()


@router.get("/api/articles")
async def read_articles(
    db_session: DbSessionDep,
    tag: str | None = None,
    author: str | None = None,
    favorited: str | None = None,
    limit: int | None = 20,
    offset: int | None = 0,
):
    statement = select(Article).offset(offset).limit(limit)
    if tag:
        statement = statement.join(ArticlesHaveTags).join(Tag).where(Tag.name == tag)
    if author:
        user_author = aliased(User, name="u_author")
        statement = statement.join(user_author).where(user_author.username == author)
    if favorited:
        fan = aliased(User, name="u_fan")
        statement = (
            statement.join(
                UsersFavourArticles,
                Article.id == UsersFavourArticles.article_id,
            )
            .join(fan)
            .where(fan.username == favorited)
        )
    articles = db_session.exec(statement).all()
    return articles


@router.get("/api/article/{slug}")
async def read_article(slug: str, db_session: DbSessionDep):
    article = db_session.exec(select(Article).where(Article.slug == slug)).first()
    if not article:
        raise HTTPException(status_code=404, detail="article not found")
    return article.tags


@router.get("/api/articles/{slug}/comments")
async def read_comments_from_article(slug: str, db_session: DbSessionDep):
    article = db_session.exec(select(Article).where(Article.slug == slug)).first()
    if not article:
        raise HTTPException(status_code=404, detail="article not found")
    comments = article.commenting_users
    return comments
