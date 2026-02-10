import os
import time
from cryptography.fernet import Fernet
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_decrypted_creds():
    """Decrypts credentials stored in the .env file."""
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("Encryption Key missing in .env")

    cipher_suite = Fernet(key.encode())

    # Decrypt email and password
    email = cipher_suite.decrypt(os.getenv("ENCRYPTED_EMAIL").encode()).decode()
    password = cipher_suite.decrypt(os.getenv("ENCRYPTED_PASSWORD").encode()).decode()

    return email, password


def login_if_needed(driver):
    """Checks for an active session and logs in if the session has expired."""
    print("Navigating to portal and checking session status...")
    driver.get(os.getenv("PORTAL_URL"))

    try:
        # Check if already logged in by looking for a Dashboard-specific element
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Dashboard')]")
            )
        )
        print("Session is active. Skipping login.")
    except:
        print("Session expired or login required. Initiating login...")
        email, password = get_decrypted_creds()
        wait = WebDriverWait(driver, 10)

        # 1. Enter Email
        email_field = wait.until(EC.element_to_be_clickable((By.NAME, "user_id")))
        email_field.send_keys(email)

        # 2. Enter Password
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.send_keys(password)

        # 3. Handle 'Remember Me' Checkbox
        remember_me = driver.find_element(By.NAME, "remember_me")
        if not remember_me.is_selected():
            # JS click is safer for hidden MUI checkbox inputs
            driver.execute_script("arguments[0].click();", remember_me)

        # 4. Click Sign In
        login_btn = driver.find_element(By.XPATH, "//button[contains(., 'Sign In')]")
        login_btn.click()

        print("Login credentials submitted.")
        time.sleep(5)  # Brief wait for post-login redirect
