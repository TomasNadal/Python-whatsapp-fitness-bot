from abc import ABC, abstractmethod
from typing import Protocol, Optional, Union
import requests
import logging
from dataclasses import asdict
from flask import jsonify
import json

from .sendMessage_types import Message, TextMessage, InteractiveMessage, MediaMessage


class MessageSender(Protocol):
    def send(self, message: Message) -> bool:
        '''Send a message and return whether it was succesful'''


class WhatsappAPIClient:
    def __init__(self, access_token: str, api_version: str, phone_number_id:str):
        self.access_token = access_token
        self.api_version = api_version
        self.phone_number_id = phone_number_id
        self.base_url = f"https://graph.facebook.com/{api_version}"

    def _get_headers(self, payload: dict) -> dict:
        ''' Get headers for API response '''
        return {
            'Authorization': f'Bearer {self.access_token}',
            "Content-Type": "application/json"
        }
    
    def send_request(self, payload: dict) -> requests.Response:
        ''' Send request to whatsapp API '''
        url = f'{self.base_url}/{self.phone_number_id}/messages'

        try:
            response = requests.post(
                url, headers=self._get_headers,json = payload, timeout=10
            )  # 10 seconds timeout as an example
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.Timeout:
            logging.error("Timeout occurred while sending message")
            return jsonify({"status": "error", "message": "Request timed out"}), 408
        except requests.RequestException as e:  # This will catch any general request exception
            logging.error(f"Request failed due to: {e}")
            return jsonify({"status": "error", "message": "Failed to send message"}), 500


class WhatsappMessageSender(MessageSender):
    ''' Concrete implementation of Whatsapp Message Sender '''

    def __init__(self, api_client: WhatsappAPIClient):
        self.api_client = api_client

    def send(self, message: Message) -> bool:
        '''Send message through whatsapp API'''
        try:
            payload = message.to_dict()
            response = self.api_client.send_request(payload)
        except Exception as e:
            logging.error(f'Exception {e} while sending the message')



