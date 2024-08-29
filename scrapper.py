import logging
import os
import requests
import json
import csv
import time
import threading
from dataclasses import dataclass, field, fields, asdict
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from urllib.parse import urlencode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("API_KEY")

@dataclass
class ProductData:
    name: str = ""
    title: str = ""
    product_url: str = ""
    ad_status: bool = False
    symbol_presence: str = ""
    price_unit: str = ""
    price: float = 0.0
    real_price: float = 0.0
    rating: float = 0.0

    def __post_init__(self):
        self.check_strings_fields()
        self.convert_prices()

    def check_strings_fields(self):
        for field in fields(self):
            if isinstance(getattr(self, field.name), str):
                if getattr(self, field.name) == "":
                    setattr(self, field.name, f"No {field.name} provided")
                    continue
                value = getattr(self, field.name)
                setattr(self, field.name, value.strip())

    def convert_prices(self):
        for field_name in ['price', 'real_price']:
            value = getattr(self, field_name)
            if isinstance(value, str):
                try:
                    # Remove currency symbols and commas, then convert to float
                    cleaned_value = ''.join(char for char in value if char.isdigit() or char == '.')
                    setattr(self, field_name, float(cleaned_value))
                except ValueError:
                    setattr(self, field_name, 0.0)

def get_scrapeops_url(url, location="us"):
    payload = {
        "api_key": API_KEY,
        "url": url,
        "location": location
    }

    proxy_url = "https://proxy.scrapeops.io/v1/?" + urlencode(payload)
    return proxy_url

def searchProduct(product_name: str, page_number=1, location="us", retries: int = 3):
    tries = 0
    success = False

    while not success and tries < retries:
        try:
            url = get_scrapeops_url(
                f"https://www.amazon.com/s?k={product_name}&page={page_number}",
                location=location
            )
            response = requests.get(url, timeout=30)

            response.raise_for_status()

            if response.status_code == 200:
                logger.info(f"Successfully fetched data for {product_name}&page={page_number}")

                soup = BeautifulSoup(response.text, "html.parser")
                bad_divs = soup.find_all("div", class_="AdHolder")

                for bad_div in bad_divs:
                    bad_div.decompose()

                divs = soup.find_all("div", {"data-component-type": "s-search-result"})

                for div in divs:
                    h2 = div.find("h2")
                    if h2 and h2.text.strip():
                        title = h2.text.strip()
                        a = h2.find("a")
                        product_url = "https://www.amazon.com" + a.get("href") if a else ""
                        ad_status = "AdHolder" in div.get("class", [])

                        symbol_element = div.find("span", class_="a-price-symbol")
                        symbol_presence = symbol_element.text if symbol_element else ""

                        pricing_unit = symbol_presence
                        prices = div.find_all("span", class_="a-offscreen")
                        rating_element = div.find("span", class_="a-icon-alt")
                        rating_present = rating_element.text[0:3] if rating_element else "0.0"
                        rating = float(rating_present)

                        price_present = prices[0].text if prices else "0"
                        real_price_present = prices[1].text if len(prices) > 1 else price_present

                        product_data = ProductData(
                            name=product_name,
                            title=title,
                            product_url=product_url,
                            ad_status=ad_status,
                            symbol_presence=symbol_presence,
                            price_unit=pricing_unit,
                            price=price_present,
                            real_price=real_price_present,
                            rating=rating
                        )

                        print(product_data)

                        # Write to CSV file
                        csv_filename = f"{product_name}.csv"
                        keys = [field.name for field in fields(product_data)]
                        file_exists = os.path.exists(csv_filename) and os.path.getsize(csv_filename) > 0

                        with open(csv_filename, "a", newline="", encoding="utf-8") as output_file:
                            writer = csv.DictWriter(output_file, fieldnames=keys)

                            if not file_exists:
                                writer.writeheader()

                            writer.writerow(asdict(product_data))

                success = True
            else:
                raise Exception(f"Error fetching data: {response.status_code}")

        except requests.exceptions.RequestException as e:
            logger.warning(f"Error fetching data (attempt {tries + 1}/{retries}): {e}")
            tries += 1
            time.sleep(2)
        except Exception as e:
            logger.warning(f"Error fetching data: {e}")
            tries += 1

    if not success:
        logger.error(f"Failed to fetch data for {product_name}&page={page_number} after {retries} retries")
        return

    print(f"Exited the Scraper for {product_name}")

def thread_search_product(product_name, pages, max_workers=5, location="us", retries=3):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                searchProduct, product_name, page, location, retries
            ) for page in range(1, pages + 1)
        ]

        for future in futures:
            future.result()

def display_product_details(product_name):
    csv_filename = f"{product_name}.csv"
    if not os.path.exists(csv_filename):
        print(f"No data found for {product_name}")
        return

    with open(csv_filename, "r", newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            product_data = ProductData(
                name=row["name"],
                title=row["title"],
                product_url=row["product_url"],
                ad_status=row["ad_status"] == "True",
                symbol_presence=row["symbol_presence"],
                price_unit=row["price_unit"],
                price=float(row["price"]),
                real_price=float(row["real_price"]),
                rating=float(row["rating"])
            )
            print(f"Name: {product_data.name}")
            print(f"Title: {product_data.title}")
            print(f"Ad Status: {product_data.ad_status}")
            print(f"Symbol Presence: {product_data.symbol_presence}")
            print(f"Price Unit: {product_data.price_unit}")
            print(f"Price: {product_data.price}")
            print(f"Real Price: {product_data.real_price}")
            print(f"Rating: {product_data.rating}")
            print("-" * 40)

if __name__ == "__main__":
    PAGES = 5
    MAX_THREADS = 3
    LOCATION = "us"
    MAX_RETRIES = 5

    product_name = input("Enter the name of the product you want to search for: ")

    try:
        thread_search_product(
            product_name,
            PAGES,
            max_workers=MAX_THREADS,
            location=LOCATION,
            retries=MAX_RETRIES)
        print(f"Exited the Scraper for {product_name}")
    except Exception as e:
        logger.error(f"An error occurred while scraping {product_name}: {e}")

    display_product_details(product_name)
