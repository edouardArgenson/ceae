import os

from db.helpers import build_database_uri
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_uri = build_database_uri(
    dialect=os.environ.get("CEAE_DB_DIALECT"),
    user=os.environ.get("CEAE_DB_USER"),
    password=os.environ.get("CEAE_DB_PASSWORD"),
    host=os.environ.get("CEAE_DB_HOST"),
    dbname=os.environ.get("CEAE_DB_NAME"),
)
SQL_ENGINE = create_engine(database_uri, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=SQL_ENGINE)
