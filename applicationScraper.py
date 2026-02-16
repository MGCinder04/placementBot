from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_my_applications(driver):
    """Scrapes the 'My Applications' page MUI DataGrid."""
    apps = []
    print("Scanning applied companies...")

    try:
        wait = WebDriverWait(driver, 10)
        rows = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "MuiDataGrid-row"))
        )

        for row in rows:
            company = row.find_element(
                By.CSS_SELECTOR, '[data-field="company_name"]'
            ).text
            profile = row.find_element(By.CSS_SELECTOR, '[data-field="profile"]').text
            deadline = row.find_element(By.CSS_SELECTOR, '[data-field="deadline"]').text
            applied_on = row.find_element(
                By.CSS_SELECTOR, '[data-field="applied_on"]'
            ).text

            # Extract Resume ID from the button text (e.g., 'Resume: 53020')
            try:
                resume_text = row.find_element(
                    By.CSS_SELECTOR, '[data-field="resume"]'
                ).text
                resume_id = resume_text.replace("Resume:", "").strip()
            except:
                resume_id = "N/A"

            apps.append(
                {
                    "company": company.strip(),
                    "profile": profile.strip(),
                    "deadline": deadline.strip(),
                    "applied_on": applied_on.strip(),
                    "resume": resume_id,
                }
            )

    except Exception as e:
        print(f"Error scraping applications: {e}")

    return apps
