from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Literal

class MessageType(Enum):
    TEXT = "text"
    DOCUMENT = "document"
    INTERACTIVE = "interactive"
    STATUS = "status"

@dataclass
class Message:
    to: str  # Identificador de WhatsApp o número de teléfono del cliente
    status: str
    type: str
    messaging_product: str

    def to_dict(self) -> dict:
        """Base conversion including common fields"""
        return {
            "messaging_product": self.messaging_product,
            "recipient_type": "individual",
            "to": self.to,
            "type": self.type
        }

    def send_reply(self, content: str) -> None:
        '''Send reply to this message'''
        pass

'''
Text message and related objects
'''
@dataclass
class TextObject:
    body: str  # Body of the message
    preview_url: bool

    def to_dict(self) -> dict:
        return {'body': self.body, 'preview_url': self.preview_url}

@dataclass
class TextMessage(Message):
    '''Text message implementation'''
    text: TextObject
    
    def __post_init__(self):
        self.type = "text"

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        return {
            **base_dict,
            'text': self.text.to_dict()
        }

'''
Interactive message and related objects
'''
@dataclass
class InteractiveBodyObject:
    text: str  # 60 char max

    def to_dict(self) -> dict:
        return {"text": self.text}

@dataclass
class FooterObject:
    text: str  # 60 char max

    def to_dict(self) -> dict:
        return {"text": self.text}

@dataclass
class Row:
    id: str  # max 24 char
    title: str  # max 200 char
    description: Optional[str] = None  # max 72 char

    def __post_init__(self):
        if len(self.id) > 24:
            raise ValueError("Row ID must be 24 characters or less")
        if len(self.title) > 200:
            raise ValueError("Title must be 200 characters or less")
        if self.description and len(self.description) > 72:
            raise ValueError("Description must be 72 characters or less")
        
    def to_dict(self) -> dict:
        row_dict = {
            "id": self.id,
            "title": self.title
        }
        if self.description:
            row_dict["description"] = self.description
        return row_dict

@dataclass
class SectionObject:
    rows: Optional[List[Row]] = None
    title: Optional[str] = None  # Obligatory if there are more than 1 section

    def to_dict(self) -> dict:
        section_dict = {}
        if self.title:
            section_dict["title"] = self.title
        if self.rows:
            section_dict["rows"] = [row.to_dict() for row in self.rows]
        return section_dict

@dataclass
class ActionObject:
    sections: List[SectionObject]

    def to_dict(self) -> dict:
        return {
            'sections': [section.to_dict() for section in self.sections]
        }

@dataclass
class HeaderObject:
    type: str
    sub_text: Optional[str]

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "sub_text": self.sub_text
        }

@dataclass
class TextHeader(HeaderObject):
    text: str  # Max 60 char

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        return {
            **base_dict,
            'text': self.text
        }

@dataclass
class InteractiveObject:
    type: Literal["list"]
    action: ActionObject
    header: HeaderObject
    body: Optional[InteractiveBodyObject] = None
    footer: Optional[FooterObject] = None

    def to_dict(self) -> dict:
        interactive_dict = {
            'type': self.type,
            'action': self.action.to_dict(),
            'header': self.header.to_dict()
        }
        if self.body:
            interactive_dict['body'] = self.body.to_dict()
        if self.footer:
            interactive_dict['footer'] = self.footer.to_dict()
        return interactive_dict

@dataclass
class InteractiveMessage(Message):
    interactive: InteractiveObject

    def __post_init__(self):
        self.type = "interactive"

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        return {
            **base_dict,
            'interactive': self.interactive.to_dict()
        }

'''
Multimedia message and related objects
'''
@dataclass
class MediaMessage(Message):
    media_id: str
    media_type: str  # document, image, video, etc.
    link: Optional[str] = None  # If hosting the document on server
    filename: Optional[str] = None  # Only use with documents

    def __post_init__(self):
        self.type = self.media_type

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        media_dict = {}
        
        if self.media_id:
            media_dict["id"] = self.media_id
        elif self.link:
            media_dict["link"] = self.link
            
        if self.media_type == "document" and self.filename:
            media_dict["filename"] = self.filename

        return {
            **base_dict,
            self.media_type: media_dict
        }