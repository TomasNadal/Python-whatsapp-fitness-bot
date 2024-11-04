from typing import Protocol, Any, Type, TypeVar
from ...models.payload_models import ValidatedWebhookPayload
from pydantic import BaseModel, Field, ValidationError, TypeAdapter
import json



class ValidatorSchema(Protocol):
    def parse(self, data: str) -> ValidatedWebhookPayload: ...

class PydanticSchema(ValidatorSchema):
    def __init__(self, model: Type[ValidatedWebhookPayload]):
        self.model = model
    
    def parse(self, data: str) -> ValidatedWebhookPayload:
        try:
            payload_dict = json.loads(data)
            webhook_payload = TypeAdapter(ValidatedWebhookPayload).validate_python(payload_dict)
            return webhook_payload

        except json.JSONDecodeError as e:
            raise ValueError(f'Invalid JSON data: {str(e)}')
        except ValidationError as e:
            raise ValueError(f'Validation failed: {str(e)}')
