from sqlmodel import Session, create_engine

from app import models

sqlite_file_name = "database.db"
slqite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(slqite_url)
