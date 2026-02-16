import mysql.connector
import os
import hashlib
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Establishes a connection to the local MySQL database."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database="iitk_placement",
    )


def generate_job_hash(company, role, profile):
    """Creates a unique MD5 hash for a job based on company, role, and profile."""
    combined = f"{company}{role}{profile}".lower().replace(" ", "")
    return hashlib.md5(combined.encode()).hexdigest()


def is_job_new(job_hash):
    """Checks if a job already exists in the database using its unique hash."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM job_openings WHERE job_hash = %s", (job_hash,))
    result = cursor.fetchone()
    conn.close()
    return result is None


def add_job(company, role, profile, deadline, proforma):
    """Inserts a new job entry into the database."""
    job_hash = generate_job_hash(company, role, profile)
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT IGNORE INTO job_openings 
        (job_hash, company_name, role_name, profile_type, deadline_text, proforma_link) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (job_hash, company, role, profile, deadline, proforma)

    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    print(f"Stored in DB: {company} | {role}")


def add_application(company, profile, deadline, applied_on, resume):
    """Inserts a personal application record into the DB."""
    # Create a unique hash for the application
    combined = f"{company}{profile}{applied_on}".lower().replace(" ", "")
    app_hash = hashlib.md5(combined.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT IGNORE INTO my_applications 
        (app_hash, company_name, profile, deadline_text, applied_on, resume_id) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (app_hash, company, profile, deadline, applied_on, resume)

    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    print(f"Application Logged: {company} - {profile}")
