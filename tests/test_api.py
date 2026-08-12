from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_token():
    response = client.post(
        "/login",
        data={
            "username": "testuser@example.com",
            "password": "password123"
        }
    )

    return response.json()["access_token"]


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Library Management System is running!"
    }


def test_register():
    response = client.post(
        "/register",
        json={
           "username": "brand_new_user_839271",
	   "email": "brand_new_839271@example.com",
           "password": "password123"
        }
    )

    assert response.status_code in [200, 400]


def test_login():
    response = client.post(
        "/login",
        data={
            "username": "testuser@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_books():
    token = get_token()

    response = client.get(
        "/books",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_book():
    token = get_token()

    response = client.post(
        "/books",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Testing FastAPI",
            "author": "Test Author",
            "category": "Programming",
            "quantity": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Testing FastAPI"
    assert data["author"] == "Test Author"
    assert "id" in data


def test_update_book():
    token = get_token()

    create_response = client.post(
        "/books",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Book To Update",
            "author": "Test Author",
            "category": "Programming",
            "quantity": 2
        }
    )

    book_id = create_response.json()["id"]

    response = client.put(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Updated Book",
            "author": "Updated Author",
            "category": "Technology",
            "quantity": 10
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Book"


def test_delete_book():
    token = get_token()

    create_response = client.post(
        "/books",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Book To Delete",
            "author": "Test Author",
            "category": "Programming",
            "quantity": 1
        }
    )

    book_id = create_response.json()["id"]

    response = client.delete(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"


def test_books_without_token():
    response = client.get("/books")

    assert response.status_code in [401, 403]