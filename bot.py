import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Load local config from .env
load_dotenv()


def init_driver():
    print("Initializing Edge Driver...")
    edge_options = Options()

    # 1. Point to the Edge Binary
    edge_options.binary_location = os.getenv("EDGE_BINARY")

    # 2. Use your existing profile to bypass login screens
    # Ensure Edge is CLOSED before running the script
    edge_options.add_argument(f"--user-data-dir={os.getenv('USER_DATA_DIR')}")
    edge_options.add_argument(f"--profile-directory={os.getenv('PROFILE_DIR')}")

    # 3. Stealth settings to avoid "Automation" banners
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option("useAutomationExtension", False)

    # 4. Set up the service using webdriver-manager
    # This automatically finds the correct EdgeDriver version for you
    service = Service(EdgeChromiumDriverManager().install())

    try:
        driver = webdriver.Edge(service=service, options=edge_options)
        return driver
    except Exception as e:
        print(f"Failed to start Edge: {e}")
        print("TIP: Make sure all Edge windows are closed before running!")
        return None


def check_for_jobs(driver):
    print(f"Navigating to: {os.getenv('PORTAL_URL')}")
    driver.get(os.getenv("PORTAL_URL"))

    # Let the page load
    time.sleep(5)

    # Logic for scraping the table will go here next
    print("Page Title:", driver.title)


if __name__ == "__main__":
    bot = init_driver()

    if bot:
        check_for_jobs(bot)

        # Keep it open for a bit to verify the login state
        print("Verification window open. Closing in 10 seconds...")
        time.sleep(10)
        bot.quit()
