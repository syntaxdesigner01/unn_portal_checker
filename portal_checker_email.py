import requests
import time
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

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
EMAIL_ADDRESS = "akpanjoseph2021@gmail.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_LIST = [
    "akpanjoseph2021@gmail.com",
    "ugochiblessing@gmail.com",
    "promisechinonso385@gmail.com"
    "christabeleze066@gmail.com"
]
CHECK_INTERVAL = 5 * 60
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

link :https://schmgr.unn.edu.ng/LoginHostel.aspx?sent=e01a1733-1f93-4214-b6a5-7964ae2eda21

Wishing you smooth success ✨
— Portal Watcher
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

log("🌙 UNN Portal Watcher started...", "blue")

while True:
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            send_email()
            log("✅ Portal is back — emails sent!", "green")
            break
        else:
            now_str = datetime.now().strftime("%I:%M %p")
            next_check = datetime.fromtimestamp(time.time() + CHECK_INTERVAL).strftime("%I:%M %p")
            log(f"😴 Still down… Checked: {now_str}, Next check: {next_check}", "yellow")
    except:
        log("🚧 No response yet…", "red" )

    time.sleep(CHECK_INTERVAL)
