import time
import json
import datetime
from plyer import notification

def load_time():
    try:
        with open("notif_time.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"hour": 8, "minute": 0}

while True:
    now = datetime.datetime.now()
    target = load_time()

    if now.hour == target["hour"] and now.minute == target["minute"]:
        notification.notify(
            title="📘 Korean Word Notifier",
            message="Check out your new word for today!",
            app_name="Korean Word Notifier",
            timeout=10
        )
        time.sleep(60)  # prevent duplicate alerts in the same minute

    time.sleep(10)
