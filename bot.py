import os
import time
from dotenv import load_dotenv

# Import our custom modules
from driverSetup import init_driver
from auth import login_if_needed

load_dotenv()


def main():
    try:
        # 1. Initialize the browser
        # All browser settings are tucked away in driver_setup.py
        bot = init_driver()

        # 2. Handle Authentication
        # All login/encryption logic is tucked away in auth.py
        login_if_needed(bot)

        # 3. Scraper Placeholder
        # This is where we will add the check_new_jobs(bot) call next
        print(f"Successfully reached: {bot.title}")

        # Keep open for a moment to verify everything is stable
        time.sleep(30)
        bot.quit()

    except Exception as e:
        print(f"An error occurred in the main loop: {e}")


if __name__ == "__main__":
    main()
