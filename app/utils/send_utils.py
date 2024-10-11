import json
from dotenv import load_dotenv
from flask import current_app
import os
import requests

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

def get_text_message_input(text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": current_app.config.get("RECIPIENT_WAID"),
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )

def send_message(text):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    data = get_text_message_input(text)

    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
        return response
    else:
        print(response.status_code)
        print(response.text)
        return response
