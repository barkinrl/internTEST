from fastapi import FastAPI, HTTPException, Depends
from dbconn import get_db
from dbconn import SessionLocal, engine
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from queries import add_new_book, get_all_books,get_book_by_id, update_book, delete_book_by_id

router = FastAPI()


class Book(BaseModel):
    id: int  #Primary key field
    name: str
    publisher: str 
    author: str
    price: float
    


# Endpoint to create a new book
@router.post("/books", response_model=Book)
async def create_book(book: Book):
    new_book = add_new_book(book.name, book.author, book.publisher, book.price)
    return new_book

# Endpoint to get all books
@router.get("/books", response_model=List[Book])
async def get_books(limit: int = 10, offset: int = 0, name: str = None, author: str = None, publisher: str = None, price_min: float = None, price_max: float = None):
    books = get_all_books(limit, offset, name, author, publisher, price_min, price_max)
    return books



# Endpoint to get a book by ID
@router.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book



# Endpoint to update a book by ID
@router.put("/books/{book_id}", response_model=Book)
async def update_book_endpoint(book_id: int, book: Book):
    updated_book = update_book(book_id, book.name, book.author, book.publisher, book.price)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book



# Endpoint to delete a book by ID
@router.delete("/books/{book_id}", response_model=Book)
async def delete_book(book_id: int):
    success = delete_book_by_id(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}