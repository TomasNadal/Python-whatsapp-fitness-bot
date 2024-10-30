from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Literal


# https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/components


''' Webhook Payload Object'''
@dataclass
class WebhookPayload:
    object: str
    entry: List['Entry']

''' Webhook Entry Object'''
@dataclass
class Entry:
    id: str
    changes: List['BaseChange']


''' Change object  '''
@dataclass
class BaseChange:
    field: Literal['messages']

@dataclass
class ChangeMessages(BaseChange):
    value: 'ValueMessageContainer'

@dataclass
class ChangeStatusContainer(BaseChange):
    value: 'StatusMessages'


''' Value object '''

@dataclass
class ValueMessageContainer:
    messaging_product: str
    metadata: 'Metadata' 
    contacts: List['Contact']
    messages: List['MessageBase']

@dataclass
class ValueStatusesContainer:
    messaging_product: str
    metadata: 'Metadata' 
    statuses: List['Status']

''' Message object '''
@dataclass
class MessageBase:
    context: Optional['Context']
    from_: str
    id: str
    timestamp: str

@dataclass
class TextMessage(MessageBase):
    type: Literal['text']
    text: 'TextMessageContent'

@dataclass
class DocumentMessage(MessageBase):
    type: Literal['document']
    document: 'DocumentMessageContent'

@dataclass
class InteractiveMessage(MessageBase):
    type: Literal['interactive']
    interactive: 'InteractiveMessageContent'

@dataclass
class Context:
    from_: str
    id:


''' Message content object '''
@dataclass
class TextMessageContent:
    body: str

@dataclass
class DocumentMessageContent:
    filename: str
    mime_type: str
    sha256: str
    id: str

@dataclass
class InteractiveMessageContent:
    type:Literal['list_reply']
    list_reply: 'ListReplyMessageContent'

@dataclass
class ListReplyMessageContent:
    id: str
    title: str
    description: str


''' Other components of the message
    - Profile
    - Contact
    - Status
    - Pricing
    - Metadata
 '''

@dataclass
class Profile:
    name: str

@dataclass
class Contact:
    profile: Profile
    wa_id: str

@dataclass
class Metadata:
    display_phone_number: str
    phone_number_id: str

@dataclass
class StatusConversationOrigin:
    type: str

@dataclass
class StatusConversation:
    id: str
    origin: StatusConversationOrigin

@dataclass
class Pricing:
    billable: bool
    pricing_model: str
    category: str

@dataclass
class Status:
    id: str
    status: str
    timestamp: str
    recipient_id: str
    conversation: StatusConversation
    pricing: Pricing

@dataclass
class ValueStatuses:
    messaging_product: str
    metadata: Metadata
    statuses: List[Status]