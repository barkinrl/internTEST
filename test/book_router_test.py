import unittest
from fastapi.testclient import TestClient
from routers.book_router import router
from database.dbconn import Base, engine
from database.schemas import BookMain
from database.queries import add_new_book, get_all_books, get_book_by_id, update_book, delete_book_by_id
from sqlalchemy.orm import Session

session = Session(engine)

client = TestClient(router)


class TestBookAPI(unittest.TestCase):
    # Setup Phase: Set up the test database and client
    def setUp(self):
        # Clear all data in the existing database
        session.query(BookMain).delete()
        self.client = client

        # Create some sample books for testing
        book1 = BookMain(name="Book 1", author="Author 1", publisher="Publisher 1", price=10.0)
        book2 = BookMain(name="Book 2", author="Author 2", publisher="Publisher 2", price=20.0)
        session.add_all([book1, book2])
        session.commit()
        self.book1_id = book1.id
        self.book2_id = book2.id



    # Teardown Phase: Clean up the test database
    def tearDown(self):
        session.query(BookMain).delete()
        session.commit()
        session.close()



    def test_get_non_existing_book(self):
        # Execute
        response = self.client.get(f"/books/12357")

        # Assert
        self.assertEqual(response.status_code, 500)


    def test_bad_request(self):
        # Setup
        invalid_book_data = {
            "author": "Test Author",
            "publisher": "Test Publisher",
            "price": 9.99
        }

        # Execute
        response = self.client.post("/books", json=invalid_book_data)

        # Assert
        self.assertEqual(response.status_code, 422)

    
    def test_create_book(self):
        # Setup
        new_book_data = {
            "name": "Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "price": 9.99
        }

        # Execute
        response = self.client.post("/books", json=new_book_data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())
        book_id = response.json()["id"]

        # Assert
        book = get_book_by_id(book_id)
        self.assertIsNotNone(book)
        self.assertEqual(book.name, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.publisher, "Test Publisher")
        self.assertEqual(book.price, 9.99)




   
    def test_get_all_books(self):
        # Execute
        response = self.client.get("/books")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 2)

        if not response.json():
            self.assertEqual(response.status_code, 404)
        
        # Assert
        books = get_all_books()
        for book in response.json():
            self.assertIn(book["name"], [b.name for b in books])



    
    def test_get_book_by_id(self):
        # Execute
        response = self.client.get(f"/books/{self.book1_id}")

        # Assert
        if response.status_code == 200:
            self.assertEqual(response.json()["id"], self.book1_id)



    
    def test_update_book(self):
        # Setup
        updated_book_data = {
            "name": "Updated Book",
            "author": "Updated Author",
            "publisher": "Updated Publisher",
            "price": 19.99
        }

        # Execute
        response = self.client.put(f"/books/{self.book1_id}", json=updated_book_data)

        # Assert
        if response.status_code == 200:
            self.assertEqual(response.json()["id"], self.book1_id)

        # Assert
        update_book(self.book1_id, **updated_book_data)
        book = get_book_by_id(self.book1_id)
        self.assertIsNotNone(book)
        self.assertEqual(book.name, "Updated Book")
        self.assertEqual(book.author, "Updated Author")
        self.assertEqual(book.publisher, "Updated Publisher")
        self.assertEqual(book.price, 19.99)

   
    def test_delete_book(self):
        # Execute
        response = self.client.delete(f"/books/{self.book1_id}")

        # Assert
        if response.status_code == 200:
            self.assertEqual(response.json()["id"], self.book1_id)


        # Assert
        delete_book_by_id(self.book1_id)
        book = get_book_by_id(self.book1_id)
        self.assertIsNone(book)


if __name__ == '__main__':
    unittest.main()



