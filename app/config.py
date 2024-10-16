import sys
import os
from dotenv import load_dotenv
import logging
from pathlib import Path


basedir = Path(__file__).parent.absolute()

class Config:
    load_dotenv()
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    YOUR_PHONE_NUMBER = os.getenv("YOUR_PHONE_NUMBER")
    APP_ID = os.getenv("APP_ID")
    APP_SECRET = os.getenv("APP_SECRET")
    RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
    VERSION = os.getenv("VERSION")
    PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")




def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )


class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{basedir / "app.db"}'
    
    # Paths and other variables
    DOWNLOAD_DATA_PATH = os.getenv("DOWNLOAD_DATA_PATH") or 'data'
    TEMPORARY_DATAFRAME_TRAINING_FILE = os.getenv("TEMPORARY_DATAFRAME_TRAINING") or 'training_data.csv'

class TestingConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TESTING_URL') or \
        f'sqlite:///{basedir / "testing.db"}'
    
    # Paths and other variables
    DOWNLOAD_DATA_PATH = os.getenv("DOWNLOAD_DATA_PATH_TESTING") or 'data'
    TEMPORARY_DATAFRAME_TRAINING_FILE = os.getenv("TEMPORARY_DATAFRAME_TRAINING_TESTING") or 'training_data.csv'
