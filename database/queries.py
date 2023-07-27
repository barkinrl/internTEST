from schemas import BookMain
from dbconn import session

import sys
print(sys.path)


# Insert a new book record
def add_new_book(book_data: BookMain):
    try:
        new_book = BookMain(
            name=book_data.name,
            author=book_data.author,
            publisher=book_data.publisher,
            price=book_data.price
        )
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
        return new_book
    finally:
        session.close()


# Query all books
def get_all_books(limit: int = 10, offset: int = 0, name: str = None, author: str = None, publisher: str = None, price_min: float = None, price_max: float = None):
    # Use the session object to perform the query
    query = session.query(BookMain)

    # Apply filters if provided
    if name:
        query = query.filter(BookMain.name.ilike(f"%{name}%"))
    if author:
        query = query.filter(BookMain.author.ilike(f"%{author}%"))
    if publisher:
        query = query.filter(BookMain.publisher.ilike(f"%{publisher}%"))
    if price_min:
        query = query.filter(BookMain.price >= price_min)
    if price_max:
        query = query.filter(BookMain.price <= price_max)

    # Apply limit and offset
    query = query.limit(limit).offset(offset)

    # Execute the query and return the results
    all_books = query.all()
    return all_books


# Function to get a book by ID
def get_book_by_id(book_id: int):
    try:
        # Use the synchronous session to query the book by ID
        return session.query(BookMain).filter(BookMain.id == book_id).first()
    finally:
        # Close the session
        session.close()


# Update a book record
def update_book(book_id: int, name: str = None, author: str = None, publisher: str = None, price: float = None):
    try:
        book = session.query(BookMain).filter(BookMain.id == book_id).first()
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
        session.commit()
        session.refresh(book)
        return book
    finally:
        session.close()


# Delete a book record
def delete_book_by_id(book_id: int):
    try:
        book = session.query(BookMain).filter(BookMain.id == book_id).first()
        if book:
            session.delete(book)
            session.commit()
            return book
        return 
    finally:
        session.close()


