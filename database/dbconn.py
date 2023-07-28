from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base


DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test3"
engine = create_engine(DATABASE_URL)

Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

