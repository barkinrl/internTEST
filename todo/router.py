from fastapi import FastAPI, HTTPException
from typing import List
from queries import add_new_book, get_all_books,get_book_by_id, update_book, delete_book_by_id
from schemas import BookMain
from basemodels import BookCreate, BookResponse, IdResponse


router = FastAPI(debug=True)


# Endpoint to create a new book
@router.post("/books", response_model=IdResponse)
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
    # Perform additional checks if needed, then return the book
    if book.id == book_id:
        return book
    else:
        raise HTTPException(status_code=400, detail="Invalid book ID")




# Endpoint to update a book by ID
@router.put("/books/{book_id}", response_model=IdResponse)
async def update_new_book(book_id: int, book: BookCreate):
    existing_book = get_book_by_id(book_id)
    
    if existing_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Perform additional checks if needed, then update the book
    if existing_book.id == book_id:
        updated_book = update_book(book_id, book)
        return updated_book
    else:
        raise HTTPException(status_code=400, detail="Invalid book ID")




# Endpoint to delete a book by ID
@router.delete("/books/{book_id}")
async def delete_book(book_id: int):
    book = get_book_by_id(book_id)
    
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Perform additional checks if needed, then delete the book
    if book.id == book_id:
        delete_book_by_id(book_id)
        return IdResponse(id=book_id)
    else:
        raise HTTPException(status_code=400, detail="Invalid book ID")