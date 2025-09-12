from sqlmodel import SQLModel

from app.db import engine


def main():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    main()
