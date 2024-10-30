from typing import Protocol
import models.payload_models as pm


class WebhookProcessor(Protocol):
    
    def process_webhook(payload: str) -> pm.WebhookPayload: 