# Uniqlo Sale Notifier Bot

Never miss a sale again. This script automatically checks your Uniqlo wishlist and sends a Telegram alert when prices drop.

---

## What It Does

This bot automates the tedious task of checking Uniqlo product pages for sales. You give it a list of items, and it runs in the background, comparing prices. If it finds an item on sale, it instantly sends a notification to your Telegram with all the details, including a convenient link to open the product directly in the Uniqlo app.

---

## Key Features

- **Automated Price Checks**: Set it up once and let it monitor prices for you.
- **Instant Telegram Alerts**: Get immediate notifications when a sale is found.
- **Track Multiple Items**: Keep your entire wishlist in one place.
- **App-Ready Links**: Tapping the notification link opens the item in the Uniqlo mobile app.
- **Lightweight & Simple**: No complex setup or databases required.

---

## How to Get Started

### Step 1: Prerequisites

- You need **Python 3** installed.
- You need the **Google Chrome** browser installed.

### Step 2: Download the Code

Clone this repository to your computer or download the files as a ZIP.

```bash
git clone <your-repository-url>
cd <repository-name>
```

### Step 3: Install Dependencies

Open your terminal or command prompt and run the following command to install the required Python libraries:

```bash
pip install selenium requests
```

### Step 4: Get ChromeDriver

The script needs a driver to control the Chrome browser.

1.  **Check your Chrome Version**: In Chrome, go to `Settings` > `About Chrome`. Note your version number (e.g., `125`).
2.  **Download Driver**: Visit the [ChromeDriver download page](https://googlechromelabs.github.io/chrome-for-testing/) and get the driver that matches your version.
3.  **Place the Driver**: Unzip the file and move the `chromedriver` executable into the same folder as the Python script.

### Step 5: Configure the Bot

Open the Python script (`.py` file) and edit the configuration section at the top.

```python
# === TELEGRAM CONFIGURATION ===
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

# === PRODUCT LIST ===
PRODUCT_URLS = [
    "[https://www.uniqlo.com/id/id/products/](https://www.uniqlo.com/id/id/products/)...", # Add your product links here
    "[https://www.uniqlo.com/id/id/products/](https://www.uniqlo.com/id/id/products/)..."
]
```

- **Bot Token**: Create a new bot by talking to [@BotFather](https://t.me/BotFather) on Telegram and paste the token here.
- **Chat ID**: Get your unique ID from [@userinfobot](https://t.me/userinfobot) on Telegram.
- **Product URLs**: Copy the full browser URLs of the Uniqlo items you want to track and add them to the list.

---

## Running the Script

To run the check manually, open a terminal in the project folder and execute:

```bash
python script.py
```

For automatic checks, you can use **Task Scheduler** on Windows or **Cron** on macOS/Linux to run the script on a daily schedule.

---

## Disclaimer

This script is for personal and educational purposes. Website structures can change, which may require updates to the script. Please use it responsibly.
