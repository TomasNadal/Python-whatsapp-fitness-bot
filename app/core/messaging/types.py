from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Literal



class MessageType(Enum):
    TEXT = "text"
    DOCUMENT = "document"
    INTERACTIVE = "interactive"
    STATUS = "status"

@dataclass
class Message:
    messaging_product: str = "whatsapp"
    status: str
    to: str # Identificador de WhatsApp o número de teléfono del cliente


    def to_dict(self) -> dict:
        """Base conversion including common fields"""
        return {
            "messaging_product": self.messaging_product,
            "recipient_type": "individual",
            "to": self.to
        }

    def send_reply(self, content: str) -> None:
        '''Send reply to this message'''

'''
Text message and related objects

'''

@dataclass
class TextMessage(Message):
    ''' Text message implementation'''
    text: 'TextObject'
    type: str = "text"


    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        return {**base_dict,
                'text': self.text.to_dict(), 'type': self.type}


@dataclass
class TextObject:
    body: str # Body of the message
    preview_url: bool = False

    def to_dict(self) -> dict:
        return {'body':self.body, 'preview_url':self.preview_url}



'''
Interactive message
'''
@dataclass
class InteractiveMessage(Message):
    type: str = "interactive"
    interactive: 'InteractiveObject'
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        return {**base_dict,
                'interactive': self.interactive.to_dict(), 'type': self.type}

@dataclass
class InteractiveObject:
    action: 'ActionObject' # Action user will do after reading message
    body: Optional['InteractiveBodyObject'] # Body of the message
    header: 'HeaderObject'
    footer: Optional['FooterObject']
    type: Literal["list"]

    def to_dict(self) -> dict:
        interactive_dict = {
            'action': self.action.to_dict(),
            'header': self.header.to_dict(),
            'type': self.type
        }
        if self.body:
            interactive_dict['body'] = self.body.to_dict()
        if self.footer:
            interactive_dict['footer'] = self.footer.to_dict()

        return interactive_dict



@dataclass
class InteractiveBodyObject:
    text: str #60 char max

    def to_dict(self) -> dict:
        return {"text": self.text}



@dataclass
class FooterObject:
    text: str #60 char max

    def to_dict(self) -> dict:
        return {"text": self.text}

    '''
    Action Object

    Right now I will only implement the "list" option
    '''
@dataclass
class ActionObject:
    sections: List['SectionObject']

    def to_dict(self) -> dict:
        section_list = [section.to_dict() for section in self.sections]
        return{
            'sections': section_list
        }


    ''' All the different Header Objects'''
@dataclass
class HeaderObject:
    sub_text: Optional[str]

    def to_dict(self) -> dict:
        return{
            'sub_text': self.sub_text
        }

@dataclass
class TextHeader(HeaderObject):
    text: str # Max 60 char

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        return{
            **base_dict,
            'text':self.text
        }

# There are more Header types not implementing them now


    ''' Section Object '''
@dataclass
class SectionObject:
    title: Optional[str] # Obligatory if there are more than 1 section
    rows: Optional[List['Row']]


    def to_dict(self) -> dict:
        section_dict = {}
        if self.title:
            section_dict["title"] = self.title
        if self.rows:
            section_dict["rows"] = [row.to_dict() for row in self.rows]
        return section_dict


@dataclass
class Row:
    id: str # max 24 char
    title: str # max 200 char
    description: Optional[str] # max 72 char

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



'''
Multimedia message and related objects

'''
@dataclass
class MediaMessage(Message):
    id = str
    link = Optional[str] # If I host the document in my server
    filename = Optional[str] # Only use with documents

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        media_dict = {}
        
        if self.id:
            media_dict["id"] = self.id
        elif self.link:
            media_dict["link"] = self.link
            
        if self.type == "document" and self.filename:
            media_dict["filename"] = self.filename

        return {
            **base_dict,
            "type": self.type,
            self.type: media_dict
        }