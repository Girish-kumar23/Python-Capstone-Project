from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import BookDatabaseManager


app = FastAPI(
    title="Book Data API"
)


db = BookDatabaseManager()


class BookCreate(BaseModel):

    title: str = Field(
        ...,
        min_length=1
    )

    price: float

    in_stock: bool

    rating: int = Field(
        ...,
        ge=1,
        le=5
    )


class BookUpdate(BaseModel):

    title: str = Field(
        ...,
        min_length=1
    )

    price: float

    in_stock: bool

    rating: int = Field(
        ...,
        ge=1,
        le=5
    )


@app.get("/")
def home():

    return {
        "message": "Book Data API is running"
    }


# GET ALL BOOKS
@app.get("/books")
def get_books():

    return db.get_all_books()


# GET ONE BOOK
@app.get("/books/{book_id}")
def get_book(book_id: int):

    book = db.get_book(book_id)

    if book is None:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


# CREATE BOOK
@app.post("/books", status_code=201)
def create_book(book: BookCreate):

    return db.create_book(
        book.title,
        book.price,
        book.in_stock,
        book.rating
    )


# UPDATE BOOK
@app.put("/books/{book_id}")
def update_book(
    book_id: int,
    book: BookUpdate
):

    updated_book = db.update_book(
        book_id,
        book.title,
        book.price,
        book.in_stock,
        book.rating
    )

    if updated_book is None:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return updated_book


# DELETE BOOK
@app.delete("/books/{book_id}")
def delete_book(book_id: int):

    deleted = db.delete_book(book_id)

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return {
        "message": "Book deleted successfully"
    }