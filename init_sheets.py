import gspread


def setup_headers():
    print("Connecting to Google Sheets...")
    # Authenticate using the JSON key
    gc = gspread.service_account(filename="google_credentials.json")
    sh = gc.open("IITK Placement Bot")

    # Define the exact headers you requested
    headers_data = {
        "Openings": [
            "Hash",
            "Company",
            "Role",
            "Profile",
            "Deadline",
            "Proforma",
            "Timestamp",
        ],
        "Applications": [
            "Hash",
            "Company",
            "Profile",
            "Deadline",
            "Applied On",
            "Resume ID",
            "Timestamp",
        ],
        "Notices": ["Hash", "Title", "Date", "Tags", "Timestamp"],
    }

    for tab_name, headers in headers_data.items():
        try:
            # Try to open the tab if it exists
            ws = sh.worksheet(tab_name)
            ws.update(values=[headers], range_name="A1")
            print(f"✅ Headers added to existing '{tab_name}' tab.")
        except gspread.exceptions.WorksheetNotFound:
            # If the tab doesn't exist, create it and add headers
            print(f"⚠️ Worksheet '{tab_name}' not found. Creating it now...")
            ws = sh.add_worksheet(title=tab_name, rows="1000", cols="20")
            ws.update(values=[headers], range_name="A1")
            print(f"✅ Created '{tab_name}' and added headers.")

    print("🎉 All headers set up successfully! Your Sheet is ready.")


if __name__ == "__main__":
    setup_headers()
