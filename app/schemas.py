from pydantic import BaseModel


# -------------------- BOOK SCHEMAS --------------------

class BookCreate(BaseModel):
    title: str
    author: str
    category: str
    quantity: int


class Book(BookCreate):
    id: int

    class Config:
        from_attributes = True


# -------------------- USER SCHEMAS --------------------

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str