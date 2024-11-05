from __future__ import annotations
from abc import ABC, abstractmethod
from app.models.payload_models import *
from app.utils.send_utils import send_message, send_interactive_list
from app.models.models import User
from app import db
from flask import current_app
from app.utils.document_utils import process_document_webhook
from app.core.messaging.validated_message_handler import MessageHandler,IdleStateMessageHandler, AddTrainingStateMessageHandler, TrainingManagementStateMessageHandler
from app.core.messaging.message_sender import WhatsappMessageSender, WhatsappAPIClient




class UserContext:
    '''
    Context class that manages states transitions for Users
    '''

    _state = None
    '''
    A reference to the current state
    '''

    # When initializing the Context, we assign a state
    def __init__(self, user: User) -> None:
        self.user = user
        self.transition_to(self.get_state_instance(user.state))


    # Get state instance of User
    def get_state_instance(self, state_name: str ) -> State:
        state_mapping = {
        'IdleState': IdleState,
        'TrainingManagementState': TrainingManagementState,
        'AddTrainingState': AddTrainingState,
        #'EstimateOneRMState': EstimateOneRMState,
        #'CreateVelocityProfileState': CreateVelocityProfileState
        # Add other states as needed
        }

        # Retrieve the state_class
        state_class = state_mapping.get(state_name)
        if not state_class:
            raise ValueError(f"State not defined {state_name}")
        
        # Instantiate the state_class setting the context to self
        state_instance = state_class(self)
        return state_instance

    # We need this back-reference to dynamically be able to change states
    def transition_to(self, state: State):
        print(f'Context: Transition from {type(self._state).__name__} to {type(state).__name__}')
        self._state = state
        self.user.state = type(state).__name__
        db.session.commit()
    '''
    Here we define the functions that we delegate to the States
    '''
    # In my case the functionality i need to delegate is the webhook management
    def handle_webhook(self, webhook):
        return self._state.handle_webhook(webhook)
    
class State(ABC):

    def __init__(self, context: UserContext = None):
        self.context = context
        self.message_handler = self._create_message_handler()

    def _create_message_handler(self) -> MessageHandler:
        """Create the appropriate message handler for this state"""
        handler_mapping = {
            'IdleState': IdleStateMessageHandler,
            'TrainingManagementState': TrainingManagementStateMessageHandler,
            'AddTrainingState': AddTrainingStateMessageHandler,
        }
        # Get current state class name
        whatsapp_api_client = WhatsappAPIClient(access_token= current_app.config.get("ACCESS_TOKEN")  , api_version= current_app.config.get("VERSION"), phone_number_id= current_app.config.get("PHONE_NUMBER_ID"))
        state_name = self.__class__.__name__
        handler_class = handler_mapping.get(state_name)
        
        if not handler_class:
            raise ValueError(f"No handler defined for state {state_name}")
            
        # Create handler with dependencies
        message_sender = WhatsappMessageSender(whatsapp_api_client) 
        return handler_class(message_sender)



    @abstractmethod
    def handle_webhook(self, webhook):
        pass

    def set_context(self, context: UserContext):
        self.context = context

class IdleState(State):

    def handle_webhook(self,webhook):
        try:
            action = self.message_handler.handle_message(webhook)
            if action == "TRAINING SELECTED":
                    self.context.transition_to(TrainingManagementState())

        except Exception as e:
            logging.ERROR(f'Unexpected exception during webhook handling {e}', exc_info=True)
            send_message("Ha habido un problema, vuelve a enviar tu mensaje.")
            

class TrainingManagementState(State):
    def handle_webhook(self,webhook):
        try:
            
            action = self.message_handler.handle_message(webhook)

            if action == "END":
                self.context.transition_to(IdleState())

            elif action == "ADD TRAINING":
                self.context.transition_to(AddTrainingState())
        
        except Exception as e:
            logging.ERROR(f"Unexpected expection {e}, returning to IDLE", exc_info=True)
            self.context.transition_to(IdleState())

class AddTrainingState(State):
    def handle_webhook(self,webhook):
        try:
            webhook_type = webhook.get_type_of_webhook()

            if webhook_type == 'text':
                text_response = webhook.get_body_of_text_message()

                if 'finitto' in text_response.lower():
                    self.context.transition_to(IdleState())

                else:
                    send_message("Manda tus datos en csv o envía finitto para acabar la sesión.")
            elif webhook_type == 'interactive':
                send_message("Ya has seleccionado una opción. Actualmente estás REGISTRANDO ENTRENAMIENTO\nPara acabar esta sesión, responde finitto")

            elif webhook_type == 'document':
                process_document_webhook(webhook, self.context.user)
                send_message("Envia más documentos o escribe finitto para acabar tu sesión")

        
        except Exception as e:
            logging.ERROR(f"Unexpected expection {e}, returning to IDLE")
            send_message("Ha habido un error con tu petición, vuelve a empezar :)")
            self.context.transition_to(IdleState())

class EstimateOneRMState(State):
    def handle_webhook(self,webhook):
        try:
            send_message("Bienvenido a tu calculadora de RM. Selecciona tu ejercicio para empezar")
            #Mandar lista de ejercicios disponibles (lo tengo que mirar en el encoder)
            
        
        except Exception as e:
            pass

"""
class CreateVelocityProfileState(State):"""