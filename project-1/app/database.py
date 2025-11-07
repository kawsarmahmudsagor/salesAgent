# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:MahesvaraBS23@db:5432/e-commerce")

engine = create_engine(DATABASE_URL)
session = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()

# Dependency
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
