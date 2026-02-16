import os
import time
from dotenv import load_dotenv

# Import our custom modular muscles
from driverSetup import init_driver
from auth import login_if_needed
from scraper import scrape_job_openings
from database import is_job_new, add_job, generate_job_hash
from notifications import send_telegram_notification

load_dotenv()


def main():
    bot = None
    try:
        # 1. Setup Driver
        bot = init_driver()

        # 2. Login & Navigate to Openings Page
        login_if_needed(bot)

        # Explicitly navigate to the job opening URL provided
        opening_url = "https://placement.iitk.ac.in/student/rc/16/opening"
        print(f"Navigating to openings page...")
        bot.get(opening_url)
        time.sleep(5)  # Allow DataGrid to populate

        # 3. Scrape Data
        found_jobs = scrape_job_openings(bot)

        # 4. Process each job
        for job in found_jobs:
            # Check if this specific combo is already in our MySQL
            job_hash = generate_job_hash(job["company"], job["role"], job["profile"])

            if is_job_new(job_hash):
                # 5. Send Notification
                success = send_telegram_notification(
                    job["company"],
                    job["role"],
                    job["profile"],
                    job["deadline"],
                    job["proforma"],
                )

                # 6. If notified, save to DB to prevent duplicate alerts
                if success:
                    add_job(
                        job["company"],
                        job["role"],
                        job["profile"],
                        job["deadline"],
                        job["proforma"],
                    )
            else:
                # Job already processed previously
                pass

        print("Automation cycle complete.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if bot:
            bot.quit()


if __name__ == "__main__":
    main()
