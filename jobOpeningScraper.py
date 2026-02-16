from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_job_openings(driver):
    """
    Scrapes the MUI DataGrid for job openings.
    Returns a list of dictionaries containing job details.
    """
    job_list = []
    print("Scanning for job rows...")

    try:
        # 1. Wait for the rows to be rendered in the DOM
        # MUI DataGrid rows always have the class 'MuiDataGrid-row'
        wait = WebDriverWait(driver, 10)
        rows = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "MuiDataGrid-row"))
        )

        for row in rows:
            # 2. Extract specific fields using CSS Selectors for the 'data-field' attribute
            # These match the headers you provided (Company, Role, Profile, etc.)
            company = row.find_element(
                By.CSS_SELECTOR, '[data-field="company_name"]'
            ).text
            role = row.find_element(By.CSS_SELECTOR, '[data-field="role"]').text
            profile = row.find_element(By.CSS_SELECTOR, '[data-field="profile"]').text
            deadline = row.find_element(By.CSS_SELECTOR, '[data-field="deadline"]').text

            # 3. Handle the 'Proforma' link
            # Usually, this is an 'a' tag or a button inside the proforma cell
            try:
                proforma_cell = row.find_element(
                    By.CSS_SELECTOR, '[data-field="proforma"]'
                )
                proforma_link = proforma_cell.find_element(
                    By.TAG_NAME, "a"
                ).get_attribute("href")
            except:
                proforma_link = "No Link Available"

            job_list.append(
                {
                    "company": company.strip(),
                    "role": role.strip(),
                    "profile": profile.strip(),
                    "deadline": deadline.strip(),
                    "proforma": proforma_link,
                }
            )

        print(f"Successfully scraped {len(job_list)} jobs.")

    except Exception as e:
        # This catch handles the "No Rows" case or if the table takes too long to load
        print("No job rows found or table timed out.")

    return job_list
