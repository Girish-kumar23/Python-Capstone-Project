import requests
from bs4 import BeautifulSoup


URL = "https://books.toscrape.com/"


RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def scrape_books():

    response = requests.get(
        URL,
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Get only the first 20 books
    book_cards = soup.select(
        "article.product_pod"
    )[:20]

    books = []

    for card in book_cards:

        # TITLE
        title = card.select_one(
            "h3 a"
        )["title"].strip()

        # PRICE
        price_text = card.select_one(
            ".price_color"
        ).get_text(strip=True)

        price_text = price_text.replace("Â£", "")
        price_text = price_text.replace("£", "")

        price = float(
            price_text.strip()
        )

        # AVAILABILITY
        availability_text = card.select_one(
            ".availability"
        ).get_text(" ", strip=True)

        in_stock = "In stock" in availability_text

        # RATING
        rating_element = card.select_one(
            "p.star-rating"
        )

        rating = 0

        if rating_element:

            classes = rating_element.get(
                "class", []
            )

            for class_name in classes:

                if class_name in RATING_MAP:

                    rating = RATING_MAP[class_name]

                    break

        books.append({
            "title": title,
            "price": price,
            "in_stock": in_stock,
            "rating": rating
        })

    return books