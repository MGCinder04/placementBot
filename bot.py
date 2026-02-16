import os
import time
from dotenv import load_dotenv

# Import our custom modular muscles
from driverSetup import init_driver
from auth import login_if_needed
from jobOpeningScraper import scrape_job_openings
from database import is_job_new, add_job, generate_job_hash
from notifications import send_telegram_notification
from applicationScraper import scrape_my_applications
from database import add_application

load_dotenv()


def main():
    bot = None
    try:
        # 1. Setup Driver
        bot = init_driver()

        # 2. Login
        login_if_needed(bot)

        # --- PART A: JOB OPENINGS ---
        opening_url = "https://placement.iitk.ac.in/student/rc/16/opening"
        print(f"Navigating to openings page: {opening_url}")
        bot.get(opening_url)
        time.sleep(10)  # Allow DataGrid to populate

        found_jobs = scrape_job_openings(bot)
        for job in found_jobs:
            job_hash = generate_job_hash(job["company"], job["role"], job["profile"])

            if is_job_new(job_hash):
                success = send_telegram_notification(
                    job["company"],
                    job["role"],
                    job["profile"],
                    job["deadline"],
                    job["proforma"],
                )
                if success:
                    add_job(
                        job["company"],
                        job["role"],
                        job["profile"],
                        job["deadline"],
                        job["proforma"],
                    )

        # --- PART B: MY APPLICATIONS ---
        app_url = "https://placement.iitk.ac.in/student/rc/16/applications"
        print(f"Navigating to applications page: {app_url}")
        bot.get(app_url)
        time.sleep(10)  # Allow DataGrid to populate

        applied_jobs = scrape_my_applications(bot)
        for app in applied_jobs:
            # add_application handles hashing and 'INSERT IGNORE' internally
            add_application(
                app["company"],
                app["profile"],
                app["deadline"],
                app["applied_on"],
                app["resume"],
            )

        # --- PART C: NOTICES (Placeholder) ---
        # notice_url = "..."
        # print("Navigating to notices...")

        print("Automation cycle complete.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if bot:
            bot.quit()


if __name__ == "__main__":
    main()
