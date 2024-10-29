import json
from dotenv import load_dotenv
from flask import jsonify
from flask import current_app
import os
import requests
import logging
from app.static.interactive_list_template import interactive_list_1, interactive_list_2

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")


def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")

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


    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"


    ''' Response <class 'requests.models.Response'>

        - status_code (int): 
        - headers (requests.structures.CaseInsensitiveDict)
        - text (str): Response content to str
        - content (bytes): Response in bytes
        - json() method: request to dict
        - url (str): Final url after redirects
    '''
    data = get_text_message_input(text)

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response

def send_interactive_list(list_option):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    if list_option == 1:
        data = interactive_list_1
    if list_option == 2:
        data = interactive_list_2  

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
    
