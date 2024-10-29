# tests/conftest.py
from app import create_app, db as _db
from app.config import TestingConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest
from .fixtures.adr_dataframes import (
    ADR_CSV,
    ADR_CSV_1
)

from .fixtures.payloads import (
    VALID_STATUS_UPDATE_PAYLOAD,
    VALID_TEXT_MESSAGE_PAYLOAD,
    VALID_DOCUMENT_MESSAGE_PAYLOAD,
    INVALID_MESSAGE_PAYLOAD,
    INTERACTIVE_LIST_SEND_PAYLOAD,
    VALID_LIST_REPLY
)

''' Defining Fixtures for testing context'''
@pytest.fixture(scope='session')
def app():
    # Creates app instance
    app = create_app(TestingConfig)
    return app

@pytest.fixture(scope='function')
def db(app):
    # Configure database for testing
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()


@pytest.fixture(scope = "function", autouse = True)
def session(db):
    """Iniciar una transacción antes de cada prueba y hacer rollback después."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db._make_scoped_session(options=options)

    db.session = session
    yield session

    transaction.rollback()
    connection.close()
    session.remove()

@pytest.fixture
def client(app):
    """Crear un cliente de prueba."""
    return app.test_client()

# Define Test Payloads
@pytest.fixture
def valid_list_reply_payload():
    return VALID_LIST_REPLY

@pytest.fixture
def interactive_send_payload():
    return INTERACTIVE_LIST_SEND_PAYLOAD


@pytest.fixture
def valid_status_update_payload():
    return VALID_STATUS_UPDATE_PAYLOAD

@pytest.fixture
def valid_text_message_payload():
    return VALID_TEXT_MESSAGE_PAYLOAD

@pytest.fixture
def valid_document_message_payload():
    return VALID_DOCUMENT_MESSAGE_PAYLOAD

@pytest.fixture
def invalid_message_payload():
    return INVALID_MESSAGE_PAYLOAD

@pytest.fixture
def adr_data():
    return ADR_CSV

@pytest.fixture
def adr_data_1():
    return ADR_CSV_1