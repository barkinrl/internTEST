from sqlalchemy import Column, Integer, String, Float
from dbconn import Base


class BookMain(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    publisher = Column(String)
    author = Column(String)
    price = Column(Float)












