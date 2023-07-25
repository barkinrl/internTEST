from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test3"
engine = create_engine(DATABASE_URL)

Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()


