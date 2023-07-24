from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from models import Book
from models import Base

# Replace these values with your PostgreSQL credentials and database name
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test3"

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create the table if it does not exist
Base.metadata.create_all(engine)


# Insert a new book record
def add_new_book(name, author, publisher, price):
    # Create a new Book object
    new_book = Book(name=name, author=author, publisher=publisher, price=price)
    
    # Add the new_book to the session
    session.add(new_book)
    
    # Commit the changes to the database
    session.commit()


# Query all books
def print_all_books():
    all_books = session.query(Book).all()
    for book in all_books:
        print(f"Book Name: {book.name}, Author: {book.author}, Publisher: {book.publisher}, Price: {book.price}")

# Update a book record
def update_book_price(book_name, new_price):
    book_to_update = session.query(Book).filter_by(name=book_name).first()
    if book_to_update:
        book_to_update.price = new_price
        session.commit()

# Delete a book record
def delete_book_by_name(book_name):
    book_to_delete = session.query(Book).filter_by(name=book_name).first()
    if book_to_delete:
        session.delete(book_to_delete)
        session.commit()

# Close the session
session.close()
