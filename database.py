import sqlite3


DATABASE_NAME = "books.db"


class BookDatabaseManager:

    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    # CREATE TABLE
    def create_table(self):

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL NOT NULL,
                in_stock BOOLEAN NOT NULL,
                rating INTEGER NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    # CREATE
    def create_book(self, title, price, in_stock, rating):

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO books
            (title, price, in_stock, rating)
            VALUES (?, ?, ?, ?)
        """, (title, price, in_stock, rating))

        book_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return self.get_book(book_id)

    # READ ALL
    def get_all_books(self):

        conn = self.get_connection()

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM books ORDER BY id")

        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]

    # READ ONE
    def get_book(self, book_id):

        conn = self.get_connection()

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM books WHERE id = ?",
            (book_id,)
        )

        row = cursor.fetchone()

        conn.close()

        if row:
            return dict(row)

        return None

    # UPDATE
    def update_book(
        self,
        book_id,
        title,
        price,
        in_stock,
        rating
    ):

        conn = self.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE books
            SET title = ?,
                price = ?,
                in_stock = ?,
                rating = ?
            WHERE id = ?
        """, (
            title,
            price,
            in_stock,
            rating,
            book_id
        ))

        updated = cursor.rowcount > 0

        conn.commit()
        conn.close()

        if updated:
            return self.get_book(book_id)

        return None

    # DELETE
    def delete_book(self, book_id):

        conn = self.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM books WHERE id = ?",
            (book_id,)
        )

        deleted = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return deleted

    # Helper method for fresh scraping
    def delete_all_books(self):

        conn = self.get_connection()

        cursor = conn.cursor()

        cursor.execute("DELETE FROM books")

        conn.commit()
        conn.close()