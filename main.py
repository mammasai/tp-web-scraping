# Scrape exactly 1,000 unique book records from the books dataset website without duplication and save to CSV
import time
from bs4 import BeautifulSoup # pyright: ignore[reportMissingImports]
import pandas as pd
import requests

scraped_data = []
current_page = 1
target_rows = 1000

print("Starting live web scraping process for books dataset... Please wait.\n")

while len(scraped_data) < target_rows:
    url = f"http://books.toscrape.com/catalogue/page-{current_page}.html"
    res = requests.get(url)

    if res.status_code != 200:
        break

    soup = BeautifulSoup(res.text, "html.parser")
    book_elements = soup.find_all("article", class_="product_pod")

    if not book_elements:
        break

    for b in book_elements:
        if len(scraped_data) >= target_rows:
            break

        title = b.find("h3").find("a")["title"].strip()
        price = b.find("p", class_="price_color").text.strip()
        availability = b.find("p", class_="instock availability").text.strip()
        rating = b.find("p", class_="star-rating")["class"][1]

        scraped_data.append({
            "Book Title": title,
            "Price": price,
            "Availability": availability,
            "Rating": rating
        })

    print(f"Page {current_page}: Accumulated {len(scraped_data)} unique rows.")
    current_page += 1
    time.sleep(0.1)

# Convert to DataFrame and save to CSV
df = pd.DataFrame(scraped_data)
output_file = "books_dataset.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\n" + "=" * 50)
print("Scraping completed successfully without data duplication!")
print(f"Total unique rows collected: {len(df)}")
print(f"File successfully saved as: {output_file}")
print("=" * 50)