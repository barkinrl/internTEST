from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from dbconn import Base


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    publisher = Column(String)
    author = Column(String)
    price = Column(Float)












