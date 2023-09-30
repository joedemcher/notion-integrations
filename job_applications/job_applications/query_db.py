import os
import requests

from notion_client import Client
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")

while NOTION_TOKEN == "":
    print("NOTION_TOKEN not found.")
    exit()

# Initialize the client
notion = Client(auth=NOTION_TOKEN)

def get_database(page_id: str) -> str:
    db = notion.databases.retrieve(database_id = page_id)
    return db

def query_database_by_date(db_id, property_name, date) -> dict:
    response = notion.databases.query(
    **{
        "database_id": db_id,
        "filter": {
            "property": property_name,
            "date": {
                "on_or_after": date,
            },
        },
    }
    )
    return response

def send_notification(title, message, priority, tags):
        requests.post("https://ntfy.sh/job_applications_alert_74618194718",
            data=message,
            headers={
                "Title": title,
                "Priority": priority,
                "Tags": tags
            })

def main():
    page_id = "a55a2edd304649d18cc86e13af7f4fdc"
    db = get_database(page_id)
    today = datetime.today()
    last_month = today - timedelta(days=30)
    date = last_month.strftime("%Y-%m-%d")
    pages = query_database_by_date(db["id"], "Submitted on", date)
    if len(pages['results']) <= 35:
        diff = 35-len(pages['results'])
        if diff > 5 and diff < 10:
            send_notification("Apply to jobs.", "Let's shoot for 3 job applications today!", "high", "inbox_tray")
        elif diff > 10:
            send_notification("Apply to jobs.", "Let's shoot for 5 job applications today!", "high", "inbox_tray")
        elif diff != 0:
            send_notification("Apply to jobs", "Let's shoot for " + str(diff) + " job applications today! ", "high", "inbox_tray")


if __name__ == "__main__":
    main()

