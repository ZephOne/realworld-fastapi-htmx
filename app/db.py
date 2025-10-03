from sqlmodel import Session, SQLModel, create_engine

from app import models

sqlite_file_name = "database.db"
slqite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(slqite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def drop_db():
    SQLModel.metadata.drop_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
