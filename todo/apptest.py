import pytest
from fastapi.testclient import TestClient
from app import router
 


client = TestClient(router)


# Test data for creating a book
new_book_data = {
    "name": "Test Book",
    "author": "Test Author",
    "publisher": "Test Publisher",
    "price": 9.99
}


# Test data for updating a book
updated_book_data = {
    "name": "Updated Book",
    "author": "Updated Author",
    "publisher": "Updated Publisher",
    "price": 19.99
}


# Test case: Create a new book
def test_create_book():
    response = client.post("/books", json=new_book_data)
    assert response.status_code == 200
    assert "id" in response.json()



# Test case: Get all books
def test_get_all_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)



# Test case: Get a book by ID
def test_get_book_by_id():
    # Create a new book
    response = client.post("/books", json=new_book_data)
    assert response.status_code == 200
    book_id = response.json()["id"]

    # Try to get the book by ID
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id



# Test case: Update a book
def test_update_book():
    # Create a new book
    response = client.post("/books", json=new_book_data)
    assert response.status_code == 200
    book_id = response.json()["id"]

    # Update the book
    response = client.put(f"/books/{book_id}", json=updated_book_data)
    assert response.status_code == 200
    assert response.json()["id"] == book_id




# Test case: Delete a book
def test_delete_book():
    # Create a new book
    response = client.post("/books", json=new_book_data)
    assert response.status_code == 200
    book_id = response.json()["id"]

    # Delete the book
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id

# Run all the test cases
if __name__ == "__main__":
    pytest.main()
