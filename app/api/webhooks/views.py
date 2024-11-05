import logging
import json
from pydantic import ValidationError
from flask import Blueprint, request, jsonify, current_app
from ...utils.whatsapp_security import verify
from ...decorators.security import signature_required
from ...utils.document_utils import process_document_webhook
from ...utils.send_utils import send_interactive_list
from ...models.models import User

from ...state.states.states import UserContext
from ... import db
from app.core.messaging.processor import WhatsappRequestProcessor
from app.core.messaging.validator import PydanticSchema, ValidatedWebhookPayload

webhook_blueprint = Blueprint("webhook", __name__)

from app.models.payload_models import *

validator = PydanticSchema(ValidatedWebhookPayload)
message_processor = WhatsappRequestProcessor(validator)


def handle_message():
    try:

        processed_payload = message_processor.process_request(request)

        if processed_payload is None:
            return jsonify({'status':'ok'}),200

        if processed_payload.is_status():
            print("STATUS WEBHOOK")
            logging.info(processed_payload)
            return jsonify({'status':'ok'}),200


        user_name, wa_id = processed_payload.get_user_contact_info()
        user = User.query.filter_by(phone_number=wa_id).one_or_none()

        if user:
            userContext = UserContext(user)
            print(user)
            print(user.state)
            userContext.handle_webhook(processed_payload)

        else:
            user = User(name = user_name, phone_number = wa_id)
            db.session.add(user)
            db.session.commit()
            userContext = UserContext(user)
            userContext.handle_webhook(processed_payload)

        db.session.commit()

        return jsonify({'status':'ok'}),200

    except ValidationError as e:
        logging.error(f"Validation failed! \n {e.json()}")
        return (
                    jsonify({"status": "error", "message": "Not a WhatsApp API event"}),
                    404,
                )
    
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON")
        return jsonify({"status": "error", "message": "Invalid JSON provided"}), 400
    
    except Exception as e:
        logging.error(f"Unexpected exception {e}", exc_info=True)
        return jsonify({"status": "error", "message": "ERROR"}), 400


@webhook_blueprint.route("/webhook", methods=["GET"])
def webhook_get():
    return verify()

@webhook_blueprint.route("/webhook", methods=["POST"])
@signature_required
def webhook_post():

    return handle_message()


