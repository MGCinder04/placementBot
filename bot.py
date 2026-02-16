import os
import time
from dotenv import load_dotenv
import re
import hashlib

# Import our custom modular muscles
from driverSetup import init_driver
from auth import login_if_needed
from jobOpeningScraper import scrape_job_openings
from database import is_job_new, add_job, generate_job_hash
from notifications import send_telegram_notification
from applicationScraper import scrape_my_applications
from database import add_application
from noticeScraper import scrape_notices
from notifications import send_notice_alert
from database import get_applied_companies, is_notice_new, add_notice

load_dotenv()


def is_company_match(notice_title, applied_companies):
    """
    Robust matching: checks if the applied company name (or its main keyword)
    is present in the notice title.
    """
    # Normalize title: remove brackets, hyphens, make lowercase
    norm_title = re.sub(r"[^a-zA-Z0-9\s]", " ", notice_title.lower())

    for company in applied_companies:
        norm_company = re.sub(r"[^a-zA-Z0-9\s]", " ", company.lower())

        # 1. Full string match attempt
        if norm_company in norm_title:
            return True

        # 2. First significant word fallback
        # (e.g., matching "Reliance" from "Reliance Retail Limited")
        words = norm_company.split()
        if len(words) > 0 and len(words[0]) > 2:
            if words[0] in norm_title.split():
                return True

    return False


def main():
    baseURL = os.getenv("PORTAL_URL").rstrip('/')
    bot = None
    try:
        # 1. Setup Driver
        bot = init_driver()

        # 2. Login
        login_if_needed(bot)

        # --- PART A: JOB OPENINGS ---
        opening_url = f"{baseURL}/student/rc/16/opening"
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
        app_url = f"{baseURL}/student/rc/16/applications"
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
        notice_url = f"{baseURL}/student/rc/16/notices"
        print(f"Navigating to notices page: {notice_url}")
        bot.get(notice_url)
        time.sleep(10)  # Allow DataGrid to populate

        applied_companies = get_applied_companies()
        portal_notices = scrape_notices(bot)

        for notice in portal_notices:
            # Generate a unique hash for the notice
            combined = f"{notice['title']}{notice['created_at']}".lower().replace(
                " ", ""
            )
            notice_hash = hashlib.md5(combined.encode()).hexdigest()

            # Check if we already processed this notice
            if is_notice_new(notice_hash):
                # Check if this notice belongs to a company you applied to
                if is_company_match(notice["title"], applied_companies):

                    success = send_notice_alert(
                        notice["title"], notice["created_at"], notice["tags"]
                    )

                    # Store in DB ONLY if it matched your applied companies
                    # so we don't notify you again
                    if success:
                        add_notice(
                            notice["title"],
                            notice["created_at"],
                            notice["tags"],
                            notice_hash,
                        )

        print("Automation cycle complete.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if bot:
            bot.quit()


if __name__ == "__main__":
    main()
