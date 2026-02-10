import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


def init_driver():
    """Initializes the Edge driver with persistent profile and stealth settings."""
    edge_options = Options()

    binary = os.getenv("EDGE_BINARY")
    user_data = os.getenv("USER_DATA_DIR")
    profile = os.getenv("PROFILE_DIR", "Default")

    if not binary or not user_data:
        raise ValueError("Critical Error: EDGE_BINARY or USER_DATA_DIR missing in .env")

    edge_options.binary_location = binary
    edge_options.add_argument(f"--user-data-dir={user_data}")
    edge_options.add_argument(f"--profile-directory={profile}")

    # Anti-detection flags
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option("useAutomationExtension", False)
    edge_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service()
    return webdriver.Edge(service=service, options=edge_options)
