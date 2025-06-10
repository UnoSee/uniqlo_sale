# -*- coding: utf-8 -*-
"""
A web scraping script to monitor product prices on the Uniqlo website.

This script automates the process of checking a predefined list of Uniqlo product
pages for sales or price drops. If any of the specified items are found to be on
sale, it compiles a summary and sends a notification to a specified Telegram
chat using a Telegram Bot.

Features:
- Checks multiple product URLs in a single run.
- Uses Selenium with a headless Chrome browser to scrape dynamic content.
- Differentiates between regular and sale prices.
- Formats a clean, readable notification message with deep links to the products.
- Suppresses unnecessary browser log messages for a cleaner console output.

Setup:
1.  Ensure you have Python installed.
2.  Install required libraries: pip install selenium requests
3.  Download the appropriate ChromeDriver for your version of Google Chrome.
4.  Configure the script by editing the "CONFIGURATION" section below:
    -   TELEGRAM_BOT_TOKEN: Your bot's token from Telegram's BotFather.
    -   TELEGRAM_CHAT_ID: Your personal or group chat ID.
    -   PRODUCT_URLS: A list of the full Uniqlo product URLs to monitor.
"""

import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- START OF CONFIGURATION ---

# === TELEGRAM CONFIGURATION ===
# 1. Paste your Bot Token from BotFather.
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
# 2. Paste your Chat ID from @userinfobot.
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

# === PRODUCT LIST ===
# Add the full web URLs of the Uniqlo products you want to monitor.
# Ensure each URL is a string and separated by a comma.
PRODUCT_URLS = [
    "https://www.uniqlo.com/id/id/products/E479169-000?colorCode=COL09&sizeCode=SMA007", # Example 1
    "https://www.uniqlo.com/id/id/products/E474437-000?colorCode=COL00&sizeCode=SMA007", # Example 2
    "https://www.uniqlo.com/id/id/products/E478913-000?colorCode=COL00&sizeCode=SMA006", # Example 3
    "https://www.uniqlo.com/id/id/products/E474432-000?colorCode=COL09&sizeCode=SMA007"
]

# --- END OF CONFIGURATION ---

# Converts a standard Uniqlo web URL to a mobile app deep link format.
# This makes the links in the notification more convenient for mobile users.
def convert_to_app_link(web_url: str) -> str:
    # Use regex to extract the product ID (e.g., E123456-000) from the URL.
    match = re.search(r'(E\d{6}-\d{3})', web_url)
    if not match:
        return web_url
    product_id = match.group(1)
    return f"https://s.uniqlo.com/id/en/product/{product_id}"

# Sends a message to the configured Telegram chat.
def send_telegram_notification(message: str):
    # Prevent sending if credentials are placeholder values.
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("--- TELEGRAM ERROR: Please set your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID. ---")
        return

    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        print("--- Notification sent successfully to Telegram! ---")
    except requests.exceptions.RequestException as e:
        print(f"--- ERROR sending notification: {e} ---")

# Navigates to a product URL and scrapes its name, price, and sale status.
def check_specific_item_price_selenium(product_url: str, driver: webdriver.Chrome) -> dict:
    product_details = {
        "name": "Name not found",
        "current_price": "Price not found",
        "is_on_sale": False,
        "original_price": None,
        "url": product_url
    }
    try:
        driver.get(product_url)
        wait = WebDriverWait(driver, 15)

        # Locate the product title.
        title_locator = (By.CSS_SELECTOR, "h1.fr-head")
        title_element = wait.until(EC.presence_of_element_located(title_locator))
        product_details['name'] = title_element.text

        # Locate the price element(s). Uniqlo pages show two prices if an
        # item is on sale (original and sale price).
        price_locator = (By.CLASS_NAME, "fr-price-currency")
        price_elements = driver.find_elements(price_locator[0], price_locator[1])

        # If two prices are found, the item is on sale.
        if len(price_elements) >= 2:
            original_price_text = price_elements[0].text.strip()
            sale_price_text = price_elements[1].text.strip()
            if original_price_text and sale_price_text:
                product_details['is_on_sale'] = True
                product_details['original_price'] = original_price_text
                product_details['current_price'] = sale_price_text
        # If one price is found, it's the standard price.
        elif len(price_elements) == 1:
            product_details['current_price'] = price_elements[0].text.strip()

        return product_details
    except Exception as e:
        print(f"      -> An error occurred while checking {product_url}: {e}")
        return product_details

# Main execution function to run the price checker.
def main():
    print(f"[{time.ctime()}] Starting multi-item price check for {len(PRODUCT_URLS)} products...")
    sale_items = []

    # --- Initialize Selenium WebDriver ---
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in the background.
    options.add_argument("--disable-gpu") # Recommended for headless mode.
    options.add_argument("--log-level=3") # Suppress console logs.
    # This experimental option further cleans up ChromeDriver's internal logs.
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=service, options=options)

    # --- Iterate Through Products and Check Prices ---
    for i, url in enumerate(PRODUCT_URLS):
        print(f"Checking item {i+1}/{len(PRODUCT_URLS)}: {url}")
        item_details = check_specific_item_price_selenium(url, driver)
        if item_details and item_details['is_on_sale']:
            sale_items.append(item_details)
        time.sleep(2)  # A small delay to avoid overwhelming the server.

    driver.quit()

    # --- Compile and Send Notification if Sales are Found ---
    if sale_items:
        print(f"\nFound {len(sale_items)} item(s) on sale! Preparing summary notification...")
        
        message_title = f"🔥 *Uniqlo Sale Alert!* 🔥\n\nYou have {len(sale_items)} item(s) on sale:\n"
        message_details = []
        
        for item in sale_items:
            app_link = convert_to_app_link(item['url'])
            detail_line = (
                f"\n*{item['name']}*\n"
                f"Now *{item['current_price']}* (was ~{item['original_price']}~)\n"
                f"[Tap to open in app]({app_link})"
            )
            message_details.append(detail_line)
            
        final_message = message_title + "\n".join(message_details)
        send_telegram_notification(final_message)
    else:
        print("\nFinished check. No items are on sale today.")

    print(f"[{time.ctime()}] Price check complete.")


if __name__ == "__main__":
    main()
