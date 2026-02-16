import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from dotenv import load_dotenv

load_dotenv()


def init_driver():
    edge_options = Options()

    # Standard anti-detection flags
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option("useAutomationExtension", False)
    edge_options.add_argument("--disable-blink-features=AutomationControlled")

    edge_binary = os.getenv("EDGE_BINARY")
    user_data_dir = os.getenv("USER_DATA_DIR")
    profile_dir = os.getenv("PROFILE_DIR", "Default")

    if edge_binary and user_data_dir:
        # --- LOCAL LAPTOP MODE ---
        # If the variables exist, we are running locally on your PC
        edge_options.binary_location = edge_binary
        edge_options.add_argument(f"user-data-dir={user_data_dir}")
        edge_options.add_argument(f"profile-directory={profile_dir}")
    else:
        # --- CLOUD SERVER MODE ---
        # If variables are missing, we are on GitHub Actions
        edge_options.add_argument("--headless=new")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        # In cloud mode, we DO NOT pass a custom user-data-dir so Edge creates a fresh temporary one

    # Selenium 4 automatically handles driver downloading if path isn't specified
    driver_path = os.getenv("EDGE_DRIVER_PATH")
    if driver_path:
        service = Service(executable_path=driver_path)
    else:
        service = Service()

    return webdriver.Edge(service=service, options=edge_options)
