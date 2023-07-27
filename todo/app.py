from fastapi import FastAPI, HTTPException
from typing import List
from queries import add_new_book, get_all_books,get_book_by_id, update_book, delete_book_by_id
from basemodels import BookCreate, BookResponse, IdResponse


router = FastAPI(debug=True)


# Endpoint to create a new book
@router.post("/books", response_model=IdResponse)
async def create_book(book: BookCreate):
    """
    This endpoint creates a new book based on the provided data in the request body.
    It expects a JSON payload with the book details (name, author, publisher, and price).

    Parameters:
        book: BookCreate - The request body model containing the book details.

    Returns:
        IdResponse: A model containing the ID of the newly created book.
    """
    try:
        new_book = add_new_book(book)
        return new_book
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating book")




# Endpoint to get all books
@router.get("/books", response_model=List[BookResponse])
async def find_books(
    limit: int = 10, 
    offset: int = 0, 
    name: str = None, 
    author: str = None, 
    publisher: str = None, 
    price_min: float = None, 
    price_max: float = None):
    """
    This endpoint retrieves a list of books based on the provided filters and pagination options.

    Parameters:
        limit: int - Maximum number of books to retrieve (default: 10).
        offset: int - Number of books to skip (default: 0).
        name: str - Filter books by name (case-insensitive).
        author: str - Filter books by author (case-insensitive).
        publisher: str - Filter books by publisher (case-insensitive).
        price_min: float - Filter books by minimum price.
        price_max: float - Filter books by maximum price.

    Returns:
        List[BookResponse]: A list of books matching the provided filters and pagination.
    """
    try:
        books = get_all_books(limit, offset, name, author, publisher, price_min, price_max)
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving books")




# Endpoint to get a book by ID
@router.get("/books/{book_id}", response_model=BookResponse)
async def find_book_by_id(book_id: int):
    """
    This endpoint retrieves a single book by its ID.

    Parameters:
        book_id: int - The ID of the book to retrieve.

    Returns:
        BookResponse: The book data matching the provided ID.

    Raises:
        HTTPException(404): If no book is found with the given ID.
    """
    try:
        book = get_book_by_id(book_id)  
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving book")




# Endpoint to update a book by ID
@router.put("/books/{book_id}", response_model=BookResponse)
async def update_new_book(book_id: int, book: BookCreate):
    """
    This endpoint updates an existing book's data based on the provided ID and request body.

    Parameters:
        book_id: int - The ID of the book to update.
        book: BookCreate - The request body model containing the updated book details.

    Returns:
        BookResponse: The updated book data.

    Raises:
        HTTPException(404): If no book is found with the given ID.
    """
    try:
        existing_book = get_book_by_id(book_id)
        
        if existing_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        
        if existing_book.id == book_id:
            updated_book = update_book(
                book_id,
                name=book.name,
                author=book.author,
                publisher=book.publisher,
                price=book.price
            )
            return updated_book
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating book")




# Endpoint to delete a book by ID
@router.delete("/books/{book_id}")
async def delete_book(book_id: int):
    """
    This endpoint deletes a book based on the provided ID.

    Parameters:
        book_id: int - The ID of the book to delete.

    Returns:
        IdResponse: A model containing the ID of the deleted book.

    Raises:
        HTTPException(404): If no book is found with the given ID.
    """
    try:
        book = get_book_by_id(book_id)
        
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        
        if book.id == book_id:
            delete_book_by_id(book_id)
            return IdResponse(id=book_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting book")

