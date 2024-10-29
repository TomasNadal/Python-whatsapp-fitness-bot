from pydantic import BaseModel, Field, ValidationError, TypeAdapter
from typing import List, Literal, Union, Annotated, Tuple
import json
import logging


''' Text Message Part'''
class TextMessageContent(BaseModel):
    preview_url: bool
    body: str

''' Interactive Message Part '''

class InteractiveHeader(BaseModel):
    type: Literal['text']
    text: str

class InteractiveBody(BaseModel):
    text: str

class InteractiveFooter(BaseModel):
    text: str

class InteractiveActionListRows(BaseModel):
    id: str
    title: str
    description: str

class InteractiveActionSections(BaseModel):
    title: str
    rows: List[InteractiveActionListRows]


class InteractiveAction(BaseModel):
    button: str
    sections: List[InteractiveActionSections]
    

class InteractiveMessageContent(BaseModel):
    type: Literal['list']
    header: InteractiveHeader
    body: InteractiveBody
    footer: InteractiveFooter
    action: InteractiveAction

'''
Add here the Information Models of each payload

'''


class SendTextPayload(BaseModel):
    messaging_product: Literal['whatsapp']
    recipient_type: Literal['individual']
    to: str
    type: Literal['text']
    text: TextMessageContent

class SendInteractivePayload(BaseModel):
    messaging_product: Literal['whatsapp']
    recipient_type: Literal['individual']
    to: str
    type: Literal['interactive']
    interactive: InteractiveMessageContent


SendPayload = Annotated[
    Union[SendTextPayload, SendInteractivePayload],
    Field(discriminator='type')
]



def parse_send_payload(payload: str) -> SendPayload | None:
    '''
    Parses the JSON payload into a SendPayload Object

    '''
    try:
        payload_dict = json.loads(payload)
        send_payload = TypeAdapter(SendPayload).validate_python(payload_dict)
        return send_payload
    except ValidationError as e:
        print("Validation failed!")
        print(e.json())
        return None
    except json.JSONDecodeError as e:
        print("JSON decoding failed!")
        print(str(e))
        return None