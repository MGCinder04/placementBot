import os
import requests
from dotenv import load_dotenv

load_dotenv()


# UPDATED: Now includes the direct link to the Openings page
def send_telegram_notification(company, role, profile, deadline, proforma_link):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    message = (
        f"🚀 *New Job Opening Detected!*\n\n"
        f"🏢 *Company:* {company}\n"
        f"💼 *Role:* {role}\n"
        f"📄 *Profile:* {profile}\n"
        f"⏳ *Deadline:* {deadline}\n\n"
        f"🔗 [View Proforma]({proforma_link})\n"
        f"🌐 [Open Portal Page](https://placement.iitk.ac.in/student/rc/16/opening)"
    )

    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except:
        return False


# NEW: Notice specific alert
def send_notice_alert(title, date, tags):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    message = (
        f"📢 *Important Notice Alert!*\n\n"
        f"📌 *Title:* {title}\n"
        f"🕒 *Date:* {date}\n"
        f"🏷️ *Tags:* {tags}\n\n"
        f"🌐 [Open Notices Page](https://placement.iitk.ac.in/student/rc/16/notices)"
    )

    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except:
        return False
