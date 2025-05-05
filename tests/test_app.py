import pytest
from app import app, books

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_books():
    # Очищаем список книг перед каждым тестом и заполняем тестовыми данными
    books.clear()
    books.extend([
        {"id": 1, "title": "Concept of Physics", "author": "H.C Verma"},
        {"id": 2, "title": "Gunahon ka Devta", "author": "Dharamvir Bharti"},
        {"id": 3, "title": "Problems in General Physsics", "author": "I.E Irodov"}
    ])

def test_get_list_of_books(client):
    response = client.get('/books')
    assert response.status_code == 200
    assert len(response.json) == 3
    assert response.json == [
        {"id": 1, "title": "Concept of Physics", "author": "H.C Verma"},
        {"id": 2, "title": "Gunahon ka Devta", "author": "Dharamvir Bharti"},
        {"id": 3, "title": "Problems in General Physsics", "author": "I.E Irodov"}
    ]

def test_successful_get_book_by_id(client):
    response = client.get('/books/1')
    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "title": "Concept of Physics",
        "author": "H.C Verma"
    }

def test_unsuccessful_get_book_by_id(client):
    response = client.get('/books/999')
    assert response.status_code == 404
    assert response.json == {"error": "Book not found"}

def test_add_book_success(client):
    new_book = {
        "id": 4,
        "title": "Eugene Onegin",
        "author": "A.S Pushkin"
    }
    response = client.post('/books', json=new_book)
    assert response.status_code == 201
    assert response.json == new_book

def test_add_book_invalid_data(client):
    response = client.post('/books', json={"title": "Invalid Book"})  # Нет id и author
    assert response.status_code >= 400 
    assert "error" in response.json

def test_update_book_success(client):
    updated_data = {
        "id": 1,
        "title": "Updated Physics",
        "author": "H.C Verma"
    }
    response = client.put('/books/1', json=updated_data)
    assert response.status_code == 200
    assert response.json == updated_data

def test_update_book_not_found(client):
    response = client.put('/books/999', json={"title": "Non-existent"})
    assert response.status_code == 404
    assert response.json == {"error": "Book not found"}

def test_delete_book_success(client):
    response = client.delete('/books/1')
    assert response.status_code == 200
    assert response.json == {"message": "Book deleted"}
    # Проверяем, что книга удалена
    response = client.get('/books/1')
    assert response.status_code == 404

def test_delete_book_not_found(client):
    response = client.delete('/books/999')
    assert response.status_code == 200  
    assert response.json == {"message": "Book deleted"}
