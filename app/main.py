from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .database import engine, Base, SessionLocal
from . import models, schemas
from .auth import hash_password, verify_password
from .jwt_handler import create_access_token
from .oauth2 import get_current_user

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home
@app.get("/")
def home():
    return {"message": "Library Management System is running!"}


# Add Book
# Add Book
@app.post("/books", response_model=schemas.Book)
def add_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_book = models.Book(
        title=book.title,
        author=book.author,
        category=book.category,
        quantity=book.quantity
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


# View All Books
@app.get("/books", response_model=list[schemas.Book])
def get_books(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(models.Book).all()


# Update Book
@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing_book = db.query(models.Book).filter(
        models.Book.id == book_id
    ).first()

    if not existing_book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    existing_book.title = book.title
    existing_book.author = book.author
    existing_book.category = book.category
    existing_book.quantity = book.quantity

    db.commit()
    db.refresh(existing_book)

    return existing_book

# Delete Book
@app.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    book = db.query(models.Book).filter(
        models.Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}


# Register User
@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        form_data.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(
        data={"sub": existing_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }