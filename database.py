import gspread
import hashlib
from datetime import datetime


# --- Connection Helper ---
def get_worksheet(tab_name):
    """Authenticates with the JSON key and opens the specific tab."""
    gc = gspread.service_account(filename="google_credentials.json")
    sh = gc.open("IITK Placement Bot")
    return sh.worksheet(tab_name)


# --- HASH GENERATORS ---
def generate_job_hash(company, role, profile):
    combined = f"{company}{role}{profile}".lower().replace(" ", "")
    return hashlib.md5(combined.encode()).hexdigest()


def generate_app_hash(company, profile):
    combined = f"{company}{profile}".lower().replace(" ", "")
    return hashlib.md5(combined.encode()).hexdigest()


# --- DUPLICATE CHECKERS ---
def is_job_new(job_hash):
    ws = get_worksheet("Openings")
    hashes = ws.col_values(1)  # Gets all existing hashes from Column A
    return job_hash not in hashes


def is_application_new(app_hash):
    ws = get_worksheet("Applications")
    hashes = ws.col_values(1)
    return app_hash not in hashes


def is_notice_new(notice_hash):
    ws = get_worksheet("Notices")
    hashes = ws.col_values(1)
    return notice_hash not in hashes


# --- ADD TO SHEETS ---
def add_job(company, role, profile, deadline, proforma):
    job_hash = generate_job_hash(company, role, profile)
    ws = get_worksheet("Openings")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([job_hash, company, role, profile, deadline, proforma, timestamp])
    print(f"Logged Job: {company}")


def add_application(company, profile, deadline, applied_on, resume_id):
    app_hash = generate_app_hash(company, profile)
    ws = get_worksheet("Applications")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row(
        [app_hash, company, profile, deadline, applied_on, resume_id, timestamp]
    )
    print(f"Logged App: {company}")


def add_notice(title, published_date, tags, notice_hash):
    ws = get_worksheet("Notices")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([notice_hash, title, published_date, tags, timestamp])
    print(f"Logged Notice: {title[:30]}...")


# --- UTILITY ---
def get_applied_companies():
    """Fetches a unique list of companies from the Applications tab."""
    try:
        ws = get_worksheet("Applications")
        companies = ws.col_values(2)  # Company names are in Column B
        unique_companies = list(set([c for c in companies if c.lower() != "company"]))
        return unique_companies
    except Exception as e:
        print(f"Could not fetch applied companies: {e}")
        return []
