from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from models import Book
from dbconn import Base
from dbconn import session
from dbconn import get_db


# Insert a new book record
def add_new_book(name, author, publisher, price):
    db = get_db
    try:
        new_book = Book(name=name, author=author, publisher=publisher, price=price)
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    finally:
        db.close()


# Query all books
def get_all_books(limit=10, offset=0, name=None, author=None, publisher=None, price_min=None, price_max=None):
    db = get_db
    try:
        query = db.query(Book)
        if name:
            query = query.filter(Book.name == name)
        if author:
            query = query.filter(Book.author == author)
        if publisher:
            query = query.filter(Book.publisher == publisher)
        if price_min is not None:
            query = query.filter(Book.price >= price_min)
        if price_max is not None:
            query = query.filter(Book.price <= price_max)

        query = query.offset(offset).limit(limit)
        books = query.all()
        return books
    finally:
        db.close()


# Function to get a book by ID
def get_book_by_id(book_id: int):
    db = get_db
    try:
        return db.query(Book).filter(Book.id == book_id).first()
    finally:
        db.close()


# Update a book record
def update_book(book_id: int, name: str = None, author: str = None, publisher: str = None, price: float = None):
    db = get_db
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            return None
        if name:
            book.name = name
        if author:
            book.author = author
        if publisher:
            book.publisher = publisher
        if price is not None:
            book.price = price
        db.commit()
        db.refresh(book)
        return book
    finally:
        db.close()


# Delete a book record
def delete_book_by_id(book_id: int):
    db = get_db
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if book:
            db.delete(book)
            db.commit()
            return True
        return False
    finally:
        db.close()


# Close the session
session.close()
