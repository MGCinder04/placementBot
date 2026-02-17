import gspread
import hashlib
from datetime import datetime

# --- Connection & Caching Helpers ---
_gc = None
_sh = None
_worksheets = {}
_cache = {}


def get_worksheet(tab_name):
    """Authenticates ONCE and caches the worksheet objects."""
    global _gc, _sh
    if _gc is None:
        _gc = gspread.service_account(filename="google_credentials.json")
        _sh = _gc.open("IITK Placement Bot")

    if tab_name not in _worksheets:
        _worksheets[tab_name] = _sh.worksheet(tab_name)
    return _worksheets[tab_name]


def get_cached_hashes(tab_name):
    """Reads hashes from the sheet ONCE and strips invisible spaces."""
    if tab_name not in _cache:
        ws = get_worksheet(tab_name)
        # Fetch column A, convert to string, remove spaces, and filter empty rows
        hashes = [str(h).strip() for h in ws.col_values(1) if str(h).strip()]
        _cache[tab_name] = set(hashes)
    return _cache[tab_name]


# --- HASH GENERATORS ---
def generate_job_hash(company, role, profile):
    combined = f"{company}{role}{profile}".lower().replace(" ", "")
    return hashlib.md5(combined.encode()).hexdigest()


def generate_app_hash(company, profile):
    combined = f"{company}{profile}".lower().replace(" ", "")
    return hashlib.md5(combined.encode()).hexdigest()


# --- DUPLICATE CHECKERS ---
def is_job_new(job_hash):
    return str(job_hash).strip() not in get_cached_hashes("Openings")


def is_application_new(app_hash):
    return str(app_hash).strip() not in get_cached_hashes("Applications")


def is_notice_new(notice_hash):
    return str(notice_hash).strip() not in get_cached_hashes("Notices")


# --- ADD TO SHEETS ---
def add_job(company, role, profile, deadline, proforma):
    job_hash = generate_job_hash(company, role, profile)
    if is_job_new(job_hash):
        ws = get_worksheet("Openings")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([job_hash, company, role, profile, deadline, proforma, timestamp])
        _cache["Openings"].add(str(job_hash).strip())
        print(f"Logged Job: {company}")


def add_application(company, profile, deadline, applied_on, resume_id):
    app_hash = generate_app_hash(company, profile)
    if is_application_new(app_hash):
        ws = get_worksheet("Applications")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row(
            [app_hash, company, profile, deadline, applied_on, resume_id, timestamp]
        )
        _cache["Applications"].add(str(app_hash).strip())
        print(f"Logged App: {company}")


def add_notice(title, published_date, tags, notice_hash):
    if is_notice_new(notice_hash):
        ws = get_worksheet("Notices")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row(
            [str(notice_hash).strip(), title, published_date, tags, timestamp]
        )
        _cache["Notices"].add(str(notice_hash).strip())
        print(f"Logged Notice: {title[:30]}...")


# --- UTILITY ---
def get_applied_companies():
    """Fetches a unique list of companies from the Applications tab."""
    try:
        ws = get_worksheet("Applications")
        companies = ws.col_values(2)
        unique_companies = list(
            set(
                [
                    str(c).strip()
                    for c in companies
                    if str(c).strip().lower() != "company"
                ]
            )
        )
        return unique_companies
    except Exception as e:
        print(f"Could not fetch applied companies: {e}")
        return []
