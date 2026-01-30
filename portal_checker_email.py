import requests
import time
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv
import keep_alive

# Keep Replit alive
keep_alive.keep_alive()

# Load env variables
load_dotenv()

def log(msg, color="default"):
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color,'')}{msg}{colors['reset']}")

# ===== CONFIG =====
URL = "https://schmgr.unn.edu.ng/LoginHostel.aspx?sent=e01a1733-1f93-4214-b6a5-7964ae2eda21"

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

EMAIL_LIST = [
    email.strip()
    for email in os.getenv("EMAIL_LIST", "").split(",")
    if email.strip()
]

CHECK_INTERVAL = 5 * 60  # 5 minutes
# ==================

def send_email():
    now = datetime.now().strftime("%I:%M %p")

    msg = EmailMessage()
    msg["Subject"] = "🎉 UNN Portal is Back Online!"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join(EMAIL_LIST)

    msg.set_content(f"""
Hi 🤍

Good news!

The UNN hostel portal is finally responding again 😌

⏰ Time: {now}
🌐 Status: Server is reachable

Please try to complete payment quickly before traffic increases.

🔗 Link:
https://schmgr.unn.edu.ng/LoginHostel.aspx?sent=e01a1733-1f93-4214-b6a5-7964ae2eda21

Wishing you smooth success ✨
— Portal Watcher
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

log("🌙 UNN Portal Watcher started...", "blue")

# 🔑 THIS IS THE KEY FIX
last_status = "down"

while True:
    try:
        response = requests.get(URL, timeout=10)

        # Optional smarter check:
        is_up = response.status_code == 200 and "Login" in response.text

        if is_up:
            if last_status == "down":
                send_email()
                log("✅ Portal just came back — email sent!", "green")
                last_status = "up"
            else:
                log("🟢 Portal still up — no alert sent", "blue")
        else:
            if last_status == "up":
                log("🔴 Portal went down again", "red")
            last_status = "down"

    except Exception:
        if last_status == "up":
            log("🔴 Portal went down again", "red")
        else:
            log("🚧 No response yet…", "yellow")
        last_status = "down"

    # Countdown UI
    for i in range(int(CHECK_INTERVAL / 60), 0, -1):
        print(f"\r⏳ Next check in {i} minute(s)...   ", end="", flush=True)
        time.sleep(60)
    print("\r", end="")
    log("🔍 Checking portal status...", "yellow")