# Web Scraper Project - README 🛠️📄

## Overview
This project is a powerful web scraper designed to search for products on Amazon and retrieve crucial details such as product name, title, price, rating, and more. The scraper is capable of fetching data across multiple pages, saving the results into a CSV file, and displaying the data directly in the terminal.

## Features 🌟
- **Multi-Page Scraping**: Fetches product details from Amazon across multiple pages.
- **Multi-Threading**: Uses threading to speed up the data fetching process.
- **CSV Export**: Saves the fetched data into a CSV file for easy access.
- **Terminal Display**: Displays the product details in the terminal in a well-organized format.

## Modules Used 🧩
1. **logging**: For logging information, warnings, and errors during the scraping process.
2. **os**: For managing environment variables and file handling.
3. **requests**: Handles HTTP requests to fetch web pages.
4. **json**: Provides functionality for parsing JSON responses (though minimally used here).
5. **csv**: Handles reading from and writing to CSV files.
6. **time**: Used to introduce delays between retries and manage timeouts.
7. **threading**: Provides threading capabilities to run concurrent scraping tasks.
8. **concurrent.futures.ThreadPoolExecutor**: Manages a pool of threads for parallel execution.
9. **dataclasses**: Creates a structured data model (`ProductData`) with automatic field handling.
10. **bs4 (BeautifulSoup)**: Parses HTML pages to extract relevant information from the web page structure.
11. **urllib.parse.urlencode**: Encodes URL parameters for the proxy service.

## Technologies Used 🛠️
### 1. **BeautifulSoup (bs4)**
   - **Purpose**: BeautifulSoup is utilized to parse the HTML content of web pages fetched from Amazon. It enables easy extraction of specific elements like product titles, prices, and ratings by navigating the HTML structure.
   - **How It’s Used**: After fetching the HTML content using the `requests` module, BeautifulSoup parses the content, and the relevant product information is extracted using methods like `find` and `find_all`.

### 2. **Threading**
   - **Purpose**: Threading is used to speed up the scraping process by enabling multiple pages to be scraped concurrently.
   - **How It’s Used**: The `ThreadPoolExecutor` from the `concurrent.futures` module manages a pool of threads. Each thread handles the scraping of a single page, significantly reducing the overall time required to scrape multiple pages.

### 3. **Data Handling (Dataclasses and CSV)**
   - **Dataclasses**: The `ProductData` class, defined as a dataclass, represents each product's information in a structured manner. It simplifies data storage and retrieval by automatically generating methods like `__init__` and `__repr__`.
   - **CSV Handling**: The `csv` module is used to write the fetched product details into a CSV file, allowing easy storage and subsequent retrieval of the data for further analysis or display.

### 4. **Proxy Service**
   - **Purpose**: A proxy service (ScrapeOps) routes the HTTP requests to Amazon, helping avoid IP bans or CAPTCHAs that could arise from frequent requests.
   - **How It’s Used**: The `get_scrapeops_url` function constructs the URL with the required parameters, including the API key, target URL, and location, and returns the proxy URL used for making the requests.

## Setup Guide 🚀
### 1. **Install Dependencies**
   Ensure you have Python installed on your system. Install the required modules by running:
   ```bash
   pip install requests beautifulsoup4
   ```

### 2. **Set Up Environment Variables**
   - Set up an environment variable `API_KEY` with your ScrapeOps API key. This key is used to access the proxy service:
     ```bash
     export API_KEY="your_scrapeops_api_key"
     ```

### 3. **Running the Script**
   - Run the script by executing:
     ```bash
     python scrapper.py
     ```
   - Enter the product name when prompted.

### 4. **Viewing Output**
   - The script will save the product details in a CSV file named after the product you searched for (e.g., `product_name.csv`).
   - The product details will also be displayed on the terminal in a formatted manner.

## Example Output 📊
Here's how the output will look in your terminal:

```
Name: Phones
Title: Samsung Galaxy A05 A055M 64GB Dual-SIM GSM Unlocked Android Smartphone (Latin America Version) - Silver
Ad Status: False
Symbol Presence: $
Price Unit: $
Price: 99.94
Real Price: 99.94
Rating: 4.2
----------------------------------------
Name: Phones
Title: OnePlus Nord N200 | 5G for T-Mobile U.S Version | 6.49" Full HD+LCD Screen | 90Hz Smooth Display | Large 5000mAh Battery | Fast Charging | 64GB Storage | Triple Camera (T-Mobile) (Renewed)
Ad Status: False
Symbol Presence: $
Price Unit: $
Price: 79.75
Real Price: 179.99
Rating: 4.1
```

## Future Enhancements 🚀
- Add error handling for common scraping issues like CAPTCHA detection.
- Implement a more sophisticated method for handling dynamic content (e.g., using Selenium).
- Expand support to scrape additional details, such as reviews or product images.

This README provides an overview of the project, including the modules used, the technologies implemented, and detailed instructions on how to set up and run the scraper. Happy scraping! 🕸️
