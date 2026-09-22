from database import BookDatabaseManager
from scraper import scrape_books


db = BookDatabaseManager()


books = scrape_books()


# Remove old records if we run the script again
db.delete_all_books()


for book in books:

    db.create_book(
        book["title"],
        book["price"],
        book["in_stock"],
        book["rating"]
    )


print(
    f"Successfully scraped and stored {len(books)} books."
)