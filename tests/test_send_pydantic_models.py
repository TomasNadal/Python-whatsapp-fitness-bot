import pytest
from pydantic import ValidationError
from app.models.payload_send_models import SendPayload, InteractiveMessageContent, parse_send_payload


def test_correctly_defined_models(interactive_send_payload):
    send_payload = parse_send_payload(interactive_send_payload)

    assert send_payload.messaging_product == "whatsapp"
    assert send_payload.to == "+16505551234"