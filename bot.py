import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Load local config from .env
load_dotenv()


def init_driver():
    chrome_options = Options()

    # Point to Brave instead of Chrome
    chrome_options.binary_location = os.getenv("BRAVE_PATH")

    # Use your profile to stay logged in
    chrome_options.add_argument(f"--user-data-dir={os.getenv('USER_DATA_DIR')}")
    chrome_options.add_argument(f"--profile-directory={os.getenv('PROFILE_DIR')}")

    # Prevent the "Chrome is being controlled by automated software" bar
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


if __name__ == "__main__":
    bot = init_driver()
    bot.get(os.getenv("PORTAL_URL"))

    # Check if we are actually logged in
    print("Page loaded. Check the browser window!")

    # Give yourself time to look, then close
    import time

    time.sleep(10)
    bot.quit()
