import unittest
from fastapi.testclient import TestClient
from routers.book_router import router


class TestBookAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(router)

    def setUp(self):
        # Test data for creating a book
        self.new_book_data = {
            "name": "Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "price": 9.99
        }

        # Test data for updating a book
        self.updated_book_data = {
            "name": "Updated Book",
            "author": "Updated Author",
            "publisher": "Updated Publisher",
            "price": 19.99
        }

    def test_create_book(self):
        response = self.client.post("/books", json=self.new_book_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["name"], self.new_book_data["name"])
        self.assertEqual(response.json()["author"], self.new_book_data["author"])
        self.assertEqual(response.json()["publisher"], self.new_book_data["publisher"])
        self.assertEqual(response.json()["price"], self.new_book_data["price"])

    def test_get_all_books(self):
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_book_by_id(self):
        # Create a new book
        response = self.client.post("/books", json=self.new_book_data)
        self.assertEqual(response.status_code, 200)
        book_id = response.json()["id"]

        # Try to get the book by ID
        response = self.client.get(f"/books/{book_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], book_id)
        self.assertEqual(response.json()["name"], self.new_book_data["name"])
        self.assertEqual(response.json()["author"], self.new_book_data["author"])
        self.assertEqual(response.json()["publisher"], self.new_book_data["publisher"])
        self.assertEqual(response.json()["price"], self.new_book_data["price"])

        # Try to get a book with an invalid ID
        response = self.client.get("/books/9999")
        self.assertEqual(response.status_code, 404)  # Not Found

    def test_update_book(self):
        # Create a new book
        response = self.client.post("/books", json=self.new_book_data)
        self.assertEqual(response.status_code, 200)
        book_id = response.json()["id"]

        # Update the book
        response = self.client.put(f"/books/{book_id}", json=self.updated_book_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], book_id)
        self.assertEqual(response.json()["name"], self.updated_book_data["name"])
        self.assertEqual(response.json()["author"], self.updated_book_data["author"])
        self.assertEqual(response.json()["publisher"], self.updated_book_data["publisher"])
        self.assertEqual(response.json()["price"], self.updated_book_data["price"])

        # Try to update a book with an invalid ID
        response = self.client.put("/books/9999", json=self.updated_book_data)
        self.assertEqual(response.status_code, 404)  # Not Found

    def test_delete_book(self):
        # Create a new book
        response = self.client.post("/books", json=self.new_book_data)
        self.assertEqual(response.status_code, 200)
        book_id = response.json()["id"]

        # Delete the book
        response = self.client.delete(f"/books/{book_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], book_id)

        # Try to delete a book with an invalid ID
        response = self.client.delete("/books/9999")
        self.assertEqual(response.status_code, 404)  # Not Found


if __name__ == "__main__":
    unittest.main()
