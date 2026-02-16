from database import get_db_connection


def setup_cloud_tables():
    print("Connecting to Aiven Cloud Database...")
    conn = get_db_connection()
    cursor = conn.cursor()

    print("Creating job_openings table...")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS job_openings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            job_hash VARCHAR(64) UNIQUE, 
            company_name VARCHAR(255) NOT NULL,
            role_name VARCHAR(255) NOT NULL,
            profile_type VARCHAR(255),
            deadline_text VARCHAR(100),
            proforma_link TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    print("Creating my_applications table...")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS my_applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            app_hash VARCHAR(64) UNIQUE, 
            company_name VARCHAR(255) NOT NULL,
            profile VARCHAR(255) NOT NULL,
            deadline_text VARCHAR(100),
            applied_on VARCHAR(100),
            resume_id VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    print("Creating portal_notices table...")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS portal_notices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            notice_hash VARCHAR(64) UNIQUE,
            title TEXT NOT NULL,
            published_date VARCHAR(100),
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.commit()
    conn.close()
    print("✅ Cloud tables created successfully! Your DB is ready.")


if __name__ == "__main__":
    setup_cloud_tables()
