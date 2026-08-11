# Library Management API

A RESTful Library Management API built with FastAPI, SQLAlchemy, SQLite, and JWT-based authentication.

## Features

- User registration
- Secure password hashing
- User login with OAuth2
- JWT access-token authentication
- Protected book endpoints
- Create, read, update, and delete books
- SQLite database
- Automatic API documentation with Swagger UI
- Postman API testing

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT
- OAuth2
- python-dotenv
- Uvicorn

## Project Structure

```text
library-management/
│
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── jwt_handler.py
│   ├── main.py
│   ├── models.py
│   ├── oauth2.py
│   └── schemas.py
│
├── .gitignore
└── README.md