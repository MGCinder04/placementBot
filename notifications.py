import os
import requests
from dotenv import load_dotenv

load_dotenv()


def send_telegram_notification(company, role, profile, deadline, proforma_link):
    """Sends a formatted Markdown message to the user via Telegram."""
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Check if we have the credentials
    if not token or not chat_id:
        print("Error: Telegram credentials missing in .env")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # Formatted message using Telegram's MarkdownV2 or HTML
    message = (
        f"🚀 *New Job Opening Detected!*\n\n"
        f"🏢 *Company:* {company}\n"
        f"💼 *Role:* {role}\n"
        f"📄 *Profile:* {profile}\n"
        f"⏳ *Deadline:* {deadline}\n\n"
        f"🔗 [View Proforma]({proforma_link})"
    )

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",  # Allows for bold text and links
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Notification sent for {company}")
            return True
        else:
            print(f"Failed to send Telegram message: {response.text}")
            return False
    except Exception as e:
        print(f"Telegram connection error: {e}")
        return False
