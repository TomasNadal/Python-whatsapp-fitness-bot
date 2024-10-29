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
    RPE_TO_PERCENTAGE_1RM_TABLE = {
    10: {
        1: 100.0, 2: 95.0, 3: 91.0, 4: 87.0, 5: 85.0, 6: 83.0, 7: 81.0, 8: 79.0
    },
    9.5: {
        1: 97.0, 2: 93.0, 3: 89.0, 4: 86.0, 5: 84.0, 6: 82.0, 7: 80.0, 8: 77.5
    },
    9: {
        1: 95.0, 2: 91.0, 3: 87.0, 4: 85.0, 5: 83.0, 6: 81.0, 7: 79.0, 8: 76.0
    },
    8.5: {
        1: 93.0, 2: 89.0, 3: 86.0, 4: 84.0, 5: 82.0, 6: 80.0, 7: 77.5, 8: 74.5
    },
    8: {
        1: 91.0, 2: 87.0, 3: 85.0, 4: 83.0, 5: 81.0, 6: 79.0, 7: 76.0, 8: 73.0
    },
    7.5: {
        1: 89.0, 2: 86.0, 3: 84.0, 4: 82.0, 5: 80.0, 6: 77.5, 7: 74.5, 8: 71.5
    },
    7: {
        1: 87.0, 2: 85.0, 3: 83.0, 4: 81.0, 5: 79.0, 6: 76.0, 7: 73.0, 8: 70.0
    }
}
    EXERCISE_V1RM = {
    "Press de banca": 0.17,
    "Remo tumbdado": 0.5,
    "Dominadas": 0.23,
    "Press militar": 0.19,
    "Jalon al pecho": 0.47,
    "Remo sentado": 0.4,
    "Sentadilla profunda": 0.3,
    "Sentadilla a la paralela": 0.3,
    "Media sentadilla": 0.3,
    "Peso muerto": 0.15,
    "Hip thrust": 0.25,
    "Prensa de pierna": 0.21,
    "Snatch": 1.04,
    "Clean": 0.9
}



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
