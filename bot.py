import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

load_dotenv()


def init_driver():
    print("Connecting to Edge...")
    edge_options = Options()

    # 1. Load and Validate Environment Variables
    binary = os.getenv("EDGE_BINARY")
    user_data = os.getenv("USER_DATA_DIR")
    profile = os.getenv("PROFILE_DIR", "Default")
    driver_path = os.getenv("EDGE_DRIVER_PATH")  # Path to your manual download

    if not binary or not user_data:
        raise ValueError(
            "Critical Error: .env variables not found. Check your .env file name and location!"
        )

    # 2. Configure Browser Options
    edge_options.binary_location = binary
    edge_options.add_argument(f"--user-data-dir={user_data}")
    edge_options.add_argument(f"--profile-directory={profile}")

    # Anti-detection and stability flags
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option("useAutomationExtension", False)
    edge_options.add_argument("--disable-blink-features=AutomationControlled")

    # 3. Service Initialization Logic
    # We check if a local driver exists first to bypass the "Offline/Host" error
    if driver_path and os.path.exists(driver_path):
        print(f"Using local driver at: {driver_path}")
        service = Service(executable_path=driver_path)
    else:
        print(
            "Local driver not found or path not set. Falling back to Network Manager..."
        )
        try:
            service = Service(EdgeChromiumDriverManager().install())
        except Exception as e:
            print(f"Network Manager failed: {e}")
            raise RuntimeError(
                "Could not start Edge. Please download msedgedriver.exe manually."
            )

    return webdriver.Edge(service=service, options=edge_options)


if __name__ == "__main__":
    try:
        # IMPORTANT: Close all Edge windows before running
        bot = init_driver()
        bot.get(os.getenv("PORTAL_URL"))
        print("Success! Staying open for 15 seconds...")
        time.sleep(15)
        bot.quit()
    except Exception as e:
        print(f"Failed: {e}")
