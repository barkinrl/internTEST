from fastapi import FastAPI, HTTPException
from typing import List
from queries import add_new_book, get_all_books,get_book_by_id, update_book, delete_book_by_id
from schemas import BookMain
from basemodels import BookCreate, BookResponse, IdResponse


router = FastAPI(debug=True)


# Endpoint to create a new book
@router.post("/books", response_model=BookResponse)
async def create_book(book: BookCreate):
    new_book = add_new_book(book)
    return new_book




# Endpoint to get all books
@router.get("/books", response_model=List[BookResponse])
async def find_books(limit: int = 10, offset: int = 0, name: str = None, author: str = None, publisher: str = None, price_min: float = None, price_max: float = None):
    books = get_all_books(limit, offset, name, author, publisher, price_min, price_max)
    return books




# Endpoint to get a book by ID
@router.get("/books/{book_id}", response_model=BookResponse)
async def find_book_by_id(book_id: int):
    book = get_book_by_id(book_id)  
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book




# Endpoint to update a book by ID
@router.put("/books/{book_id}", response_model=BookResponse)
async def put_new_book(book_id: int, book: BookCreate):
    updated_book = update_book(book_id, name=book.name, author=book.author, publisher=book.publisher, price=book.price)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book




# Endpoint to delete a book by ID
@router.delete("/books/{book_id}", response_model=IdResponse)
async def delete_book(book_id: int):
    deleted = delete_book_by_id(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted