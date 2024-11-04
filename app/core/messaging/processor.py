from typing import Protocol, Optional, Union, TypeVar, Type, Generic
import requests
from werkzeug.exceptions import BadRequest
import logging
from dataclasses import asdict
from flask import jsonify
import json
from .validator import PydanticSchema, ValidatedWebhookPayload, ValidatorSchema

class RequestProcessor(Protocol):

    def process_request(request: requests.request) -> ValidatedWebhookPayload: ...
    ''' Processes a request and returns a processed ValidatedWebhookPayload Object'''


class WhatsappRequestProcessor(RequestProcessor):

    def __init__(self, payload_validator: ValidatorSchema):
        self.payload_validator = payload_validator

    def process_request(self, request: requests.request) -> ValidatedWebhookPayload:
        payload = request.get_json()
        payload_str = json.dumps(payload)
        processed_payload = self.payload_validator.parse(data = payload_str)
        return processed_payload
