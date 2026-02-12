CREATE DATABASE IF NOT EXISTS iitk_placement;

USE iitk_placement;

CREATE TABLE job_openings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_hash VARCHAR(64) UNIQUE, 
    company_name VARCHAR(255) NOT NULL,
    role_name VARCHAR(255) NOT NULL,
    profile_type VARCHAR(255),
    deadline_text VARCHAR(100),
    proforma_link TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);