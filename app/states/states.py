from __future__ import annotations
from abc import ABC, abstractmethod
from app.models.payload_models import *
from app.utils.send_utils import send_message, send_interactive_list
from app.models.models import User
from app import db
from app.utils.document_utils import process_document_webhook

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

    @abstractmethod
    def handle_webhook(self, webhook):
        pass

    def set_context(self, context: UserContext):
        self.context = context

class IdleState(State):

    def handle_webhook(self,webhook):
        try:

            webhook_type = webhook.get_type_of_webhook()


            if webhook_type == 'text':
                body = webhook.get_body_of_text_message()
                print(f'User replied {body}')
                response_remainder = send_message("Por favor, elige una opcion de la lista")
                response_list = send_interactive_list(1)
                if response_remainder.status_code == 200 and response_list.status_code == 200:
                    print(f'Succesfully sent reminder to choose from list.')
                
                else:
                    print(f"Error sending option list {response_remainder.text}")

            elif webhook_type == 'interactive':
                message_content = webhook.get_messages_content()

                id,title = message_content.list_reply.get_list_reply_content()

                if id == 'training' and title == 'Opciones entrenamiento':
                    response_list = send_interactive_list(2)
                    self.context.transition_to(TrainingManagementState())

        except Exception as e:
            logging.ERROR(f'Unexpected exception during webhook handling {e}')
            send_message("Ha habido un problema, vuelve a enviar tu mensaje.")
            

class TrainingManagementState(State):
    def handle_webhook(self,webhook):
        try:
            webhook_type = webhook.get_type_of_webhook()

            if webhook_type == 'text':
                text_response = webhook.get_body_of_text_message()
                print(f'User replied {text_response}')
                response_remainder = send_message("Elige qué quieres hacer en tu entrenamiento")
                response_list = send_interactive_list(2)
                if 'finitto' in text_response.lower():
                    self.context.transition_to(IdleState())

            elif webhook_type == 'interactive':
                message_content = webhook.get_messages_content()

                id,title = message_content.list_reply.get_list_reply_content()

                if id == 'add_training' and title == 'Añade un entrenamiento':
                    self.context.transition_to(AddTrainingState())
                else:
                    send_message("Selecciona otra opción, esta aun no está lista.")
        
        except Exception as e:
            logging.ERROR(f"Unexpected expection {e}, returning to IDLE")
            send_message("Ha habido un error con tu petición, vuelve a seleccionar la opción")
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