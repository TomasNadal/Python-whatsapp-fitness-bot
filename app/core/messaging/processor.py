from typing import Protocol, Optional, Union
import requests
import logging
from dataclasses import asdict
from flask import jsonify
from ...models.payload_models import ValidatedWebhookPayload
from webhookTypes import WebhookPayload


class RequestProcessor(Protocol):

    def process_request(request: requests.request) -> WebhookPayload: ...
    ''' Processes a request and returns a processed WebhookPayload Object'''


class PayloadValidator(Protocol):

    def process_payload(payload: str) -> WebhookPayload: ...
    ''' Processes a payload and returns the processed WebhookPayload'''


class WhatsappPayloadValidator(Protocol):

    def process_payload()


class WhatsappRequestProcessor(RequestProcessor):

    def __init__(self, payload_validator: PayloadValidator):
        self.payload_validator = payload_validator

    def process_request(self, request: requests.request) -> WebhookPayload:
        payload = request.get_json()

        processed_payload = self.payload_validator.process_payload(payload)

