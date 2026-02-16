from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_notices(driver):
    """Scrapes the Notices page."""
    notices = []
    print("Scanning for notices...")

    try:
        wait = WebDriverWait(driver, 10)
        rows = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "MuiDataGrid-row"))
        )

        for row in rows:
            created_at = row.find_element(
                By.CSS_SELECTOR, '[data-field="CreatedAt"]'
            ).text
            title = row.find_element(By.CSS_SELECTOR, '[data-field="title"]').text
            tags = row.find_element(By.CSS_SELECTOR, '[data-field="tags"]').text

            notices.append(
                {
                    "created_at": created_at.strip(),
                    "title": title.strip(),
                    "tags": tags.strip(),
                }
            )

        print(f"Successfully scraped {len(notices)} notices.")
    except Exception as e:
        print("No notices found or table timed out.")

    return notices
