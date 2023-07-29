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
        book1 = BookMain(name="Book 1 Name", author="Author 1", publisher="Publisher 1", price=19.99)
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
        response = self.client.get(f"/books/9876")

        # Assert
        self.assertEqual(response.status_code, 404)


    def test_create_book_bad_request(self):
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

        all_books = get_all_books()
        
        # Assert
        for book in response.json():
            self.assertIn("id", book)
            self.assertIn("name", book)
            self.assertIn("author", book)
            self.assertIn("publisher", book)
            self.assertIn("price", book)

            # Find the corresponding book in the database
            corresponding_book = next((b for b in all_books if b.id == book["id"]), None)
            self.assertIsNotNone(corresponding_book)

            # Assert individual fields
            self.assertEqual(book["name"], corresponding_book.name)
            self.assertEqual(book["author"], corresponding_book.author)
            self.assertEqual(book["publisher"], corresponding_book.publisher)
            self.assertEqual(book["price"], corresponding_book.price)



    
    def test_get_book_by_id(self):
        # Execute
        response = self.client.get(f"/books/{self.book1_id}")

        # Assert
        self.assertEqual(response.status_code, 200)
        book_data = response.json()

        # Assert 
        self.assertEqual(book_data["id"], self.book1_id)
        self.assertEqual(book_data["name"], "Book 1 Name")  
        self.assertEqual(book_data["author"], "Author 1")  
        self.assertEqual(book_data["publisher"], "Publisher 1")  
        self.assertEqual(book_data["price"], 19.99)


    
    def test_update_book(self):
        # Setup
        updated_book_data = {
            "name": "Updated Book",
            "author": "Updated Author",
            "publisher": "Updated Publisher",
            "price": 21.00
        }   

        # Execute
        response = self.client.put(f"/books/{self.book1_id}", json=updated_book_data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.book1_id)

        # Assert
        update_book(self.book1_id, **updated_book_data)
        book = get_book_by_id(self.book1_id)
        self.assertIsNotNone(book)
        self.assertEqual(book.name, "Updated Book")
        self.assertEqual(book.author, "Updated Author")
        self.assertEqual(book.publisher, "Updated Publisher")
        self.assertEqual(book.price, 21.00)

   
    def test_delete_book(self):
        # Execute
        response = self.client.delete(f"/books/{self.book1_id}")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.book1_id)



if __name__ == '__main__':
    unittest.main()



