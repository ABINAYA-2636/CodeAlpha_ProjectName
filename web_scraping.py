import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def get_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print("Error:", e)
        return None

def scrape_books(pages=5):
    data = []
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"

    for page in range(1, pages + 1):
        print(f"Scraping page {page}")
        soup = get_soup(base_url.format(page))
        if not soup:
            continue

        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price_text = book.find("p", class_="price_color").text
            price = float(price_text.replace("£", "").replace("Â", ""))

            rating_text = book.find("p", class_="star-rating")["class"][1]
            rating = RATING_MAP.get(rating_text, 0)

            data.append({
                "Title": title,
                "Price (£)": price,
                "Rating (1-5)": rating,
                "Scraped_On": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        time.sleep(1)

    return pd.DataFrame(data)

def save_files(df):
    df.to_csv("smart_books_data.csv", index=False)
    df.to_excel("smart_books_data.xlsx", index=False)

def analyze(df):
    print("\nTotal Books:", len(df))
    print("Average Price:", round(df["Price (£)"].mean(), 2))
    print("Top Rated Books:")
    print(df[df["Rating (1-5)"] == 5][["Title", "Price (£)"]].head())

def main():
    print("SMART BOOK PRICE INTELLIGENCE SYSTEM")
    df = scrape_books()

    if not df.empty:
        save_files(df)
        analyze(df)
        print("\nData saved successfully!")
    else:
        print("No data scraped.")

if __name__ == "__main__":
    main()
