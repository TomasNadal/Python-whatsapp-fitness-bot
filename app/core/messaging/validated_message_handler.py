from typing import Protocol, Optional
from .validator import ValidatedWebhookPayload
from .message_sender import WhatsappMessageSender, MessageSender
from app.static.interactive_list_template import interactive_list_1, interactive_list_2
from app.utils.document_utils import download_adr_document_from_webhook

class MessageHandler(Protocol):
    def handle_message(self, validated_message: ValidatedWebhookPayload) -> None: ...


class IdleStateMessageHandler(MessageHandler):
    '''
    Returns 
        "TRAINING_SELECTED if transition to TrainingManagementState
        None if not valid transition 
    
    '''

    def __init__(self, message_sender: MessageSender):
        self.message_sender = message_sender

    def handle_message(self, validated_message: ValidatedWebhookPayload) -> Optional[str]:
        webhook_type = validated_message.get_type_of_webhook()

        if webhook_type == 'text':
            action = self._handle_text(validated_message)
            return action
            
        elif webhook_type == 'interactive':
            action = self._handle_interactive(validated_message)
            return action

        return None

    def _handle_text(self, validated_message: ValidatedWebhookPayload) -> None:
        body = validated_message.get_body_of_text_message()

        print(f'User replied {body}')
        self.message_sender.send("Por favor, elige una opcion de la lista")
        self.message_sender.send(interactive_list_1)


    def _handle_interactive(self, validated_message: ValidatedWebhookPayload) -> Optional[str]:
        message_content = validated_message.get_messages_content()
        id,title = message_content.list_reply.get_list_reply_content()

        if id == 'training' and title == 'Opciones entrenamiento':
            response_list = self.message_sender.send(interactive_list_2)
            return "TRAINING SELECTED"


class TrainingManagementStateMessageHandler(MessageHandler):
    def __init__(self, message_sender: MessageSender):
        self.message_sender = message_sender

    def handle_message(self, validated_message: ValidatedWebhookPayload) -> Optional[str]:
        webhook_type = validated_message.get_type_of_webhook()
        try:
            if webhook_type == 'text':
                action = self._handle_text(validated_message)
                return action
                
            elif webhook_type == 'interactive':
                action = self._handle_interactive(validated_message)
                return action

            return None
        
        except Exception as e:
            self.message_sender("Ha habido un error con tu petición, vuelve a seleccionar la opción")
            raise Exception(f"Unexpected error {str(e)}")

    def _handle_text(self, validated_message: ValidatedWebhookPayload) -> Optional[str]:
        body = validated_message.get_body_of_text_message()
        print(f'User replied {body}')
        if 'finitto' in body.lower():
            return "END"
        else:
            self.message_sender.send("Elige qué quieres hacer en tu entrenamiento")
            self.message_sender.send(interactive_list_2)


    def _handle_interactive(self, validated_message: ValidatedWebhookPayload) -> Optional[str]:
        message_content = validated_message.get_messages_content()
        id,title = message_content.list_reply.get_list_reply_content()

        if id == 'add_training' and title == 'Añade un entrenamiento':
            return "ADD TRAINING"
        else:
            self.message_sender.send("Selecciona otra opción, esta aun no está lista.")



class AddTrainingStateMessageHandler(MessageHandler):
    def __init__(self, message_sender: MessageSender):
        self.message_sender = message_sender

    def handle_message(self, validated_message: ValidatedWebhookPayload) -> Optional[str]:
        webhook_type = validated_message.get_type_of_webhook()
        try:
            if webhook_type == 'text':
                self._handle_text(validated_message)
                return None
                
            elif webhook_type == 'interactive':
                action = self._handle_interactive(validated_message)
                return action
            
            elif webhook_type == 'document':
                document_path = self._handle_document(validated_message)
                if document_path:
                    self.message_sender.send("ADR document recibido correctamente")
                    return document_path

                return None
            

            return None
        
        except Exception as e:
            self.message_sender.send("Ha habido un error con tu petición, vuelve a seleccionar la opción")
            raise Exception(f"Unexpected error {str(e)}")

    def _handle_text(self, validated_message: ValidatedWebhookPayload) -> Optional[str]:
        body = validated_message.get_body_of_text_message()
        print(f'User replied {body}')
        if 'finitto' in body.lower():
            return "END"
        else:
            self.message_sender.send("Manda tus datos en csv o envía finitto para acabar la sesión.")
            self.message_sender.send(interactive_list_2)


    def _handle_interactive(self, validated_message: ValidatedWebhookPayload) -> Optional[str]:
        self.message_sender.send("Ya has seleccionado una opción. Actualmente estás REGISTRANDO ENTRENAMIENTO\nPara acabar esta sesión, responde finitto")

    def _handle_document(self, validated_message: ValidatedWebhookPayload) -> Optional[str]:
        download_path = download_adr_document_from_webhook(validated_message)
        return download_path