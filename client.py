import requests
import pandas as pd
import matplotlib.pyplot as plt


API_URL = "http://127.0.0.1:8000"


def fetch_books():

    response = requests.get(
        f"{API_URL}/books",
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def main():

    books = fetch_books()


    # Convert JSON into DataFrame
    df = pd.DataFrame(books)


    # Print DataFrame
    print("\n===== BOOK DATA =====\n")

    print(df)


    # Export CSV
    df.to_csv(
        "exported_books.csv",
        index=False
    )

    print(
        "\nCSV exported as exported_books.csv"
    )


    # Create scatter plot
    plt.figure(
        figsize=(8, 5)
    )

    plt.scatter(
        df["price"],
        df["rating"]
    )


    plt.title(
        "Book Price vs Rating"
    )

    plt.xlabel(
        "Price (£)"
    )

    plt.ylabel(
        "Rating (1-5)"
    )

    plt.grid(True)

    plt.tight_layout()


    # Save chart
    plt.savefig(
        "price_vs_rating.png"
    )

    print(
        "Scatter plot saved as price_vs_rating.png"
    )


if __name__ == "__main__":
    main()