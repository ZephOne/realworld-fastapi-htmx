from datetime import datetime

from pydantic import EmailStr, FilePath
from sqlmodel import Relationship, SQLModel, Field


class UsersFollowUsers(SQLModel, table=True):
    user_followed_id: int = Field(foreign_key="user.id", primary_key=True)
    user_following_id: int = Field(foreign_key="user.id", primary_key=True)


class UsersFavourArticles(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    article_id: int = Field(foreign_key="article.id", primary_key=True)


class UsersCommentArticles(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    article_id: int = Field(foreign_key="article.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default=None)
    body: str

    commenting_user: "User" = Relationship(back_populates="commented_articles")
    commented_article: "Article" = Relationship(back_populates="commenting_users")


class ArticlesHaveTags(SQLModel, table=True):
    article_id: int = Field(foreign_key="article.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    password_hash: str
    username: str = Field(unique=True, index=True, max_length=40)
    bio: str | None = None
    image: FilePath | None = Field(default=None, unique=True)

    followers: list["User"] = Relationship(
        back_populates="following", link_model=UsersFollowUsers
    )
    following: list["User"] = Relationship(
        back_populates="followers", link_model=UsersFollowUsers
    )

    favorite_articles: list["Article"] = Relationship(
        back_populates="favoriting_users", link_model=UsersFavourArticles
    )

    commented_articles: list["UsersCommentArticles"] = Relationship(
        back_populates="commenting_user", link_model=UsersCommentArticles
    )


class Article(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(unique=True)
    title: str
    description: str
    body: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default=None)

    author_id: int = Field(foreign_key="user.id")

    favoriting_users: list["Article"] = Relationship(
        back_populates="favorite_articles", link_model=UsersFavourArticles
    )

    commenting_users: list["UsersCommentArticles"] = Relationship(
        back_populates="commented_article"
    )

    tags: list["Tag"] = Relationship(
        back_populates="articles", link_model=ArticlesHaveTags
    )


class Tag(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str

    articles: list["Article"] = Relationship(
        back_populates="tags", link_model=ArticlesHaveTags
    )
