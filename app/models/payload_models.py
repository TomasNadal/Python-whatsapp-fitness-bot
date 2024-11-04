from pydantic import BaseModel, Field, ValidationError, TypeAdapter
from typing import List, Literal, Union, Annotated, Tuple, Optional
import json
import logging

# https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/components

class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str

# Status models
class StatusConversationOrigin(BaseModel):
    type: str

class StatusConversation(BaseModel):
    id: str
    origin: StatusConversationOrigin

class Pricing(BaseModel):
    billable: bool
    pricing_model: str
    category: str

class Status(BaseModel):
    id: str
    status: str
    timestamp: str
    recipient_id: str
    conversation: StatusConversation
    pricing: Pricing

class ValueStatuses(BaseModel):
    messaging_product: str
    metadata: Metadata
    statuses: List[Status]

'''
Message Models
'''
class Profile(BaseModel):
    name: str

class Contact(BaseModel):
    profile: Profile
    wa_id: str

'''
Different types of message
'''
class TextMessageContent(BaseModel):
    body: str

class DocumentMessageContent(BaseModel):
    filename: str
    mime_type: str
    sha256: str
    id: str

class ListReplyMessageContent(BaseModel):
    id: str
    title: str
    description: str

    def get_list_reply_content(self):
        id = self.id
        title = self.title

        return id, title

# There can be more InteractiveMessages but I will leave this as this for now
class InteractiveMessageContent(BaseModel):
    type:Literal['list_reply']
    list_reply: ListReplyMessageContent

# Context Model
class Context(BaseModel):
    from_: str = Field(..., alias='from')
    id: str

class MessageBase(BaseModel):
    context: Optional[Context] = None
    from_: str = Field(..., alias='from')
    id: str
    timestamp: str

    model_config = dict(populate_by_name=True)

class TextMessage(MessageBase):
    type: Literal['text']
    text: TextMessageContent

class DocumentMessage(MessageBase):
    type: Literal['document']
    document: DocumentMessageContent

class InteractiveMessage(MessageBase):
    type: Literal['interactive']
    interactive: InteractiveMessageContent


# Use discriminated union based on the 'type' field
Message = Annotated[Union[TextMessage, DocumentMessage,InteractiveMessage], Field(discriminator='type')]

# Messages Value
class ValueMessages(BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: List[Contact]
    messages: List[Message]

# Change Models
class ChangeMessages(BaseModel):
    field: Literal['messages']
    value: ValueMessages

class ChangeStatuses(BaseModel):
    field: Literal['messages']  # 'field' remains 'messages' for statuses as per payload
    value: ValueStatuses

# Union of Change Types Without Discriminator
Change = Union[ChangeMessages, ChangeStatuses]



# ---------------------------
# Webhook Models
# ---------------------------


class Entry(BaseModel):
    id: str
    changes: List[Change]

class ValidatedWebhookPayload(BaseModel):
    object: str
    entry: List[Entry]


    def get_changes(self) -> Change:
        changes = self.entry[0].changes[0]
        return changes
    
    def get_value(self):
        changes = self.get_changes()
        value = changes.value

        return value
    
    def get_user_contact_info(self):
        value = self.get_value()
        contacts = value.contacts[0]
        user_name = contacts.profile.name
        wa_id = contacts.wa_id
        return user_name, wa_id
    
    def get_messages(self):
        value = self.get_value()
        messages = value.messages[0]

        return messages
    
    def get_messages_content(self):
        value = self.get_value()
        messages = value.messages[0]
        
        if isinstance(messages, InteractiveMessage):
            return messages.interactive
        
        if isinstance(messages, DocumentMessage):
            return messages.document
        
        if isinstance(messages, TextMessage):
            return messages.text
        return messages

    def get_display_phone_number(self) -> str:
        value = self.get_value()
        display_phone_number = value.metadata.display_phone_number

        return display_phone_number
    
    # Returns type of message (document,text,audio...)
    def get_message_type(self) -> str:
        messages = self.get_messages()

        return messages.type

    #Probably better to just extract it from type
    def get_type_of_webhook(self) -> str:
        change = self.get_changes()

        if isinstance(change,ChangeStatuses):
            return 'status'
        elif isinstance(change,ChangeMessages):
            return self.get_message_type()
        else:
            return 'unknown'

    def is_message(self) -> bool:
        change = self.get_changes()
        return isinstance(change,ChangeMessages)
    
    def is_status(self) -> bool:
        change = self.get_changes()
        return isinstance(change,ChangeStatuses)
    
    def is_text_message(self) -> bool:
        change = self.get_changes()

        if not isinstance(change,ChangeMessages):
            return logging.error("Not a message")
        
        message = change.value.messages[0]
        return isinstance(message, TextMessage)

    def is_document_message(self) -> bool:
        change = self.get_changes()

        if not isinstance(change,ChangeMessages):
            return logging.error("Not a message")
        
        message = change.value.messages[0]
        return isinstance(message, DocumentMessage)

    # Not really useful just for testing 
    def get_phone_status(self) -> tuple:
        if self.is_status():
            values = self.get_value()
            phone = self.get_display_phone_number()
            statuses = values.statuses[0]
            status = statuses.status
            
            return (phone,status)

    def get_body_of_text_message(self) -> str:
        if self.is_text_message():
            change = self.get_changes()
            message = change.value.messages[0]
            body = message.text.body
            return body
        else:
            return "Not a message"


    def get_document_of_document_message(self) -> DocumentMessageContent:
        if self.is_document_message():
            change = self.get_changes()
            message = change.value.messages[0]
            document = message.document

        return document
    
    def get_from_id_timestamp(self):
        change = self.get_changes()
        message = change.value.messages[0]
        from_ = message.from_
        id = message.id
        timestamp = message.timestamp

        return from_,id,timestamp
     
    

