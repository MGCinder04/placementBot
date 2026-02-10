import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

load_dotenv()


def init_driver():
    edge_options = Options()

    # Path configuration from .env
    binary = os.getenv("EDGE_BINARY")
    user_data = os.getenv("USER_DATA_DIR")
    profile = os.getenv("PROFILE_DIR", "Default")

    if not binary or not user_data:
        raise ValueError("Critical Error: EDGE_BINARY or USER_DATA_DIR missing in .env")

    edge_options.binary_location = binary

    # Persistent session configuration
    edge_options.add_argument(f"--user-data-dir={user_data}")
    edge_options.add_argument(f"--profile-directory={profile}")

    # Stealth and anti-detection flags
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option("useAutomationExtension", False)
    edge_options.add_argument("--disable-blink-features=AutomationControlled")

    # Native Selenium Manager automatically handles driver matching/downloading
    service = Service()

    driver = webdriver.Edge(service=service, options=edge_options)
    return driver


def check_portal(driver):
    url = os.getenv("PORTAL_URL")
    print(f"Navigating to {url}...")
    driver.get(url)

    # Initial wait for page load and login session verification
    time.sleep(5)
    print(f"Current Page: {driver.title}")


if __name__ == "__main__":
    try:
        # Ensure all Edge instances are closed before running
        bot = init_driver()
        check_portal(bot)

        # Keep open for verification
        time.sleep(15)
        bot.quit()
    except Exception as e:
        print(f"Bot failed: {e}")
