import pandas as pd
from datetime import datetime, timezone, timedelta
import hashlib
from flask import current_app
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models.models import User, TrainingSession, TrainingDetail, Exercise
from .path_utils import get_download_data_path
import logging

# Configure a dedicated logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels of logs

# You can add handlers here if needed, for example, to log to a file
# handler = logging.FileHandler('app.log')
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)



'''
All these functions are to pre-process the csv data

'''
def split_series_column(df):
    '''
    This column splits the series columns. If the series is "-" it means data was taken outside
    measured series so most likely an error
    '''
    logger.debug("Entering split_series_column function.")
    new_df = df.copy()

    boolean_mask = new_df["SERIE"] != "-"
    new_df = new_df[boolean_mask]

    try:
        
        logger.debug("DataFrame copied successfully.")
        
        # Extract REP and SERIE using regex
        new_df["REP"] = new_df["SERIE"].str.extract(r'R(\d+)')
        new_df["SERIE"] = new_df["SERIE"].str.extract(r'S(\d+)')
        logger.info("Successfully split 'SERIE' column into 'SERIE' and 'REP'.")
        
        return new_df
    except Exception as e:
        logger.error(f"Exception in split_series_column: {e}", exc_info=True)
        raise  # Re-raise exception after logging

def remove_columns(df):
    '''Removes some unnecessary columns in the data'''
    new_df = df.copy()
    try:
        new_df.drop(["Perfil","Ecuacion"], axis = 1)

        return new_df

    except Exception as e:
        logger.error(f"Exception in split_series_column: {e}", exc_info=True)
        raise  # Re-raise exception after logging


def create_hash_id(row, columns):
    logger.debug("Creating hash ID for a row.")
    try:
        values = [str(row[col]) for col in columns]
        combined = '_'.join(values)
        hash_id = hashlib.md5(combined.encode()).hexdigest()[:8]
        logger.debug(f"Hash ID created: {hash_id} for combined values: {combined}")
        return hash_id
    except Exception as e:
        logger.error(f"Exception in create_hash_id: {e}", exc_info=True)
        raise

def add_hash_ids(df, columns_to_hash):
    logger.debug("Adding hash IDs to DataFrame.")
    try:
        df["hash_id"] = df.apply(lambda row: create_hash_id(row, columns_to_hash), axis=1)
        logger.info("Hash IDs added successfully.")
        return df
    except Exception as e:
        logger.error(f"Exception in add_hash_ids: {e}", exc_info=True)
        raise

def change_columns_type(df, columns, type_list):
    logger.debug("Changing column types.")
    try:
        if len(columns) != len(type_list):
            logger.error("The length of 'columns' and 'type_list' must be the same.")
            raise ValueError("The length of 'columns' and 'type_list' must be the same.")

        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            logger.error(f"Missing columns in DataFrame: {missing_columns}")
            raise KeyError(f"The following columns are not in the DataFrame: {missing_columns}")

        df_converted = df.copy()
        logger.debug("DataFrame copied for type conversion.")

        for col, target_type in zip(columns, type_list):
            try:
                logger.debug(f"Converting column '{col}' to type '{target_type}'.")
                if target_type == 'category':
                    df_converted[col] = df_converted[col].astype('category')
                elif target_type == 'datetime':
                    df_converted[col] = pd.to_datetime(df_converted[col], errors='coerce')
                elif target_type == 'numeric':
                    df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')
                else:
                    df_converted[col] = df_converted[col].astype(target_type)
                logger.info(f"Column '{col}' converted to '{target_type}'.")
            except ValueError as ve:
                logger.error(f"ValueError: Cannot convert column '{col}' to {target_type}. {ve}", exc_info=True)
            except TypeError as te:
                logger.error(f"TypeError: Invalid type specified for column '{col}'. {te}", exc_info=True)
            except Exception as e:
                logger.error(f"Unexpected error converting column '{col}': {e}", exc_info=True)

        return df_converted
    except Exception as e:
        logger.error(f"Exception in change_columns_type: {e}", exc_info=True)
        raise

def add_timestamps(df):
    logger.debug("Adding timestamps to DataFrame.")
    try:
        if not isinstance(df, pd.DataFrame):
            logger.error("Input is not a pandas DataFrame.")
            raise TypeError("Input must be a pandas DataFrame.")

        if df.empty:
            logger.error("Input DataFrame is empty. Cannot add timestamps.")
            raise ValueError("Input DataFrame is empty. Cannot add timestamps.")

        df_converted = df.copy()
        current_datetime = pd.Timestamp(datetime.now(timezone.utc))
        df_converted['Timestamp'] = current_datetime
        logger.info("Timestamp added successfully.")
        return df_converted
    except Exception as e:
        logger.error(f"Exception in add_timestamps: {e}", exc_info=True)
        raise

def reorder_columns(df):
    logger.debug("Reordering DataFrame columns.")
    try:
        column_order = [
            'Timestamp',
            'SERIE',
            'REP',
            'KG',
            'D',
            'VM',
            'VMP',
            'RM',
            'P(W)',
            'Ejer.',
            'Atleta',
            'hash_id'
        ]

        missing_cols = [col for col in column_order if col not in df.columns]
        if missing_cols:
            logger.error(f"Missing columns in DataFrame: {missing_cols}")
            raise ValueError(f"Missing columns in DataFrame: {missing_cols}")

        df_reordered = df[column_order]
        logger.info("Columns reordered successfully.")

        raw_to_db_column_mapping = {
            'Timestamp': 'timestamp',
            'SERIE': 'serie',
            'REP': 'rep',
            'KG': 'kg',
            'D': 'd',
            'VM': 'vm',
            'VMP': 'vmp',
            'RM': 'rm',
            'P(W)': 'p_w',
            'Ejer.': 'ejercicio',
            'hash_id': 'hash_id'
        }

        renamed_adr_csv = df_reordered.rename(columns=raw_to_db_column_mapping)
        logger.info("Columns renamed successfully.")
        return renamed_adr_csv
    except Exception as e:
        logger.error(f"Exception in reorder_columns: {e}", exc_info=True)
        raise

def preprocess_adr_data(new_adr_path):
    logger.debug(f"Preprocessing ADR data from path: {new_adr_path}")
    try:
        new_data = pd.read_csv(new_adr_path)
        logger.info("CSV data read successfully.")

        new_data_copy = new_data.copy()
        new_data_copy = new_data_copy.drop(columns="R")
        logger.debug("Column 'R' dropped successfully.")


        new_data_copy = split_series_column(new_data_copy)


        columns_to_hash = ['SERIE', 'REP', 'KG', 'D', 'VM', 'VMP', 'RM', 'P(W)', 'Ejer.', 'Atleta']
        new_data_copy = add_hash_ids(new_data_copy, columns_to_hash)

        columns = ['SERIE', 'REP', 'KG', 'D', 'VM', 'VMP', 'RM', 'P(W)']
        type_list = ['int', 'int', 'float', 'float', 'float', 'float', 'float', 'float']
        new_data_copy = change_columns_type(new_data_copy, columns, type_list)

        new_data_copy = add_timestamps(new_data_copy)

        new_data_copy = reorder_columns(new_data_copy)

        logger.info("ADR data preprocessed successfully.")
        return new_data_copy
    except Exception as e:
        logger.error(f"Exception in preprocess_adr_data: {e}", exc_info=True)
        raise

def filter_df_based_on_hash(old_df, new_df):
    logger.debug("Filtering new DataFrame based on existing hash IDs.")
    try:
        # Ensure 'hash_id' exists in old_df
        if 'hash_id' in old_df.columns:
            # Drop NaN values to avoid including them in the hash set
            existing_hashes = set(old_df['hash_id'].dropna())
            logger.debug(f"Number of existing hashes: {len(existing_hashes)}")
        else:
            logger.warning("'hash_id' column not found in old_df. Assuming no existing hashes.")
            existing_hashes = set()

        # Ensure 'hash_id' exists in new_df
        if 'hash_id' not in new_df.columns:
            logger.error("'hash_id' column not found in new_df.")
            raise KeyError("'hash_id' column is missing in the new DataFrame.")

        # Perform the filtering
        new_series_condition = ~new_df['hash_id'].isin(existing_hashes)
        new_series_df = new_df[new_series_condition]
        logger.info(f"Filtered DataFrame to {len(new_series_df)} new records.")
        return new_series_df
    except Exception as e:
        logger.error(f"Exception in filter_df_based_on_hash: {e}", exc_info=True)
        raise

'''
These functions provide info from the database
'''

"""
def get_previous_adr_data():
    logger.debug("Retrieving previous ADR data.")
    try:
        file_path = get_download_data_path() / current_app.config.get('TEMPORARY_DATAFRAME_TRAINING')
        if file_path.exists():
            adr_dataframe = pd.read_csv(file_path)
            logger.info(f"Previous ADR data loaded from {file_path}.")
        else:
            adr_dataframe = pd.DataFrame(columns=[
                'timestamp',
                'serie',
                'rep',
                'kg',
                'd',
                'vm',
                'vmp',
                'rm',
                'p_w',
                'perfil',
                'ejercicio',
                'atleta',
                'Ecuacion',
                'hash_id'
            ])
            adr_dataframe.to_csv(file_path, index=False)
            logger.info(f"No existing ADR data found. Created new DataFrame and saved to {file_path}.")
        return adr_dataframe
    except Exception as e:
        logger.error(f"Exception in get_previous_adr_data: {e}", exc_info=True)
        raise
"""

"""
def get_user_from_df(df) -> User:
    logger.debug("Retrieving user from DataFrame.")
    try:
        atleta_alias = df.loc[1, "Atleta"]
        logger.debug(f"Atleta alias extracted: {atleta_alias}")

        query = sa.select(User).where(User.alias == atleta_alias)
        result = db.session.scalars(query).all()
        logger.debug(f"Number of users found: {len(result)}")

        if not result:
            logger.error(f"User with alias '{atleta_alias}' not found in the database.")
            raise KeyError("User not found in the database.")

        logger.info(f"User '{atleta_alias}' retrieved successfully.")
        return result[0]
    except Exception as e:
        logger.error(f"Exception in get_user_from_df: {e}", exc_info=True)
        raise
"""

def add_or_return_training_session(user) -> TrainingSession:
    logger.debug(f"Adding or retrieving training session for user ID: {user.id}")
    try:
        time_now = datetime.now(timezone.utc)
        time_limit = time_now - timedelta(hours=3)
        logger.debug(f"Current time: {time_now}, Time limit: {time_limit}")

        query = sa.select(TrainingSession).where(
            TrainingSession.user_id == user.id,
            TrainingSession.created_at >= time_limit,
            TrainingSession.created_at <= time_now
        )

        sessions = db.session.scalars(query).all()
        logger.debug(f"Number of existing sessions found: {len(sessions)}")

        if not sessions:
            training_session = TrainingSession(user=user)
            db.session.add(training_session)
            db.session.commit()
            logger.info(f"New training session created for user ID: {user.id}")
            return training_session

        logger.info(f"Existing training session returned for user ID: {user.id}")
        return sessions[0]
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error in add_or_return_training_session: {e}", exc_info=True)
        raise


# Adds the information to the database
def add_dataframe_to_training_detail(df, user, training_session):
    logger.debug(f"Adding DataFrame to TrainingDetail for session ID: {training_session.id}")
    try:
        temp_dict_ejercicio_id = {}
        for index, row in df.iterrows():
            if row['ejercicio'] not in temp_dict_ejercicio_id:
                query = sa.select(Exercise).where(
                    Exercise.name == row['ejercicio']
                )

                query_results = db.session.execute(query).scalars().all()
                print(query_results)
                if not query_results:
                    new_exercise = Exercise(name = row['ejercicio'])
                    db.session.add(new_exercise)
                    db.session.flush()  # This will assign the ID without committing
                    ejercicio_id = new_exercise.id  # Now you can access the ID
                    temp_dict_ejercicio_id[row['ejercicio']] = ejercicio_id
                else:  
                    ejercicio_id = query_results[0].id
                    temp_dict_ejercicio_id[row['ejercicio']] = ejercicio_id
            else:
                ejercicio_id = temp_dict_ejercicio_id[row['ejercicio']]

            training_detail = TrainingDetail(
                session_id=training_session.id,
                timestamp=row['timestamp'],
                serie=row['serie'],
                rep=row['rep'],
                kg=row['kg'],
                d=row['d'],
                vm=row['vm'],
                vmp=row['vmp'],
                rm=row['rm'],
                p_w=row['p_w'],
                ejercicio_id=ejercicio_id,
                atleta_id=user.id,
                hash_id=row['hash_id']
            )
            db.session.add(training_detail)
            logger.debug(f"Added TrainingDetail record for hash_id: {row['hash_id']}")
        db.session.commit()
        logger.info(f"All records from DataFrame added to TrainingDetail for session ID: {training_session.id}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Exception in add_dataframe_to_training_detail: {e}", exc_info=True)
        raise

# Gets the training details of a training session and puts them in a dataframe
def get_training_detail_to_dataframe(user, training_session):
    logger.debug(f"Fetching TrainingDetail records for user ID: {user.id} and session ID: {training_session.id}")
    try:
        query = sa.select(TrainingDetail).where(
            sa.and_(
                TrainingDetail.atleta_id == user.id,
                TrainingDetail.session_id == training_session.id
            )
        )

        query_results = db.session.execute(query).scalars().all()
        logger.debug(f"Number of TrainingDetail records fetched: {len(query_results)}")

        data = []
        for detail in query_results:
            data.append({
                'id': detail.id,
                'session_id': detail.session_id,
                'timestamp': detail.timestamp,
                'serie': detail.serie,
                'rep': detail.rep,
                'kg': detail.kg,
                'd': detail.d,
                'vm': detail.vm,
                'vmp': detail.vmp,
                'rm': detail.rm,
                'p_w': detail.p_w,
                'ejercicio': detail.ejercicio,
                'atleta_id': detail.atleta_id,
                'hash_id': detail.hash_id
            })
        logger.info("TrainingDetail records converted to DataFrame successfully.")
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        logger.error(f"Exception in get_training_detail_to_dataframe: {e}", exc_info=True)
        raise



'''
Combined function
'''
def process_incoming_training_data(document_path, user):
    logger.debug(f"Processing incoming training data from path: {document_path}")
    try:
        # Preprocess the incoming ADR data
        adr_data_processed = preprocess_adr_data(document_path)
        logger.debug("ADR data preprocessed successfully.")

        # Retrieve the user associated with the data
        logger.debug(f"User retrieved: {user.alias} (ID: {user.id})")

        # Add or retrieve an existing training session for the user
        training_session = add_or_return_training_session(user)
        logger.debug(f"Training session ID: {training_session.id}")

        # Fetch existing training details from the database
        db_dataframe = get_training_detail_to_dataframe(user, training_session)
        logger.debug(f"Database DataFrame fetched with {len(db_dataframe)} records.")

        # Filter out records that already exist in the database
        new_reps_df = filter_df_based_on_hash(db_dataframe, adr_data_processed)
        logger.debug(f"Filtered new reps DataFrame has {len(new_reps_df)} new records.")

        # Check if there are new records to add
        if not new_reps_df.empty:
            add_dataframe_to_training_detail(new_reps_df, user, training_session)
            logger.info("Incoming training data processed and added to the database successfully.")


        else:
            logger.info("No new training records to add to the database.")

        return new_reps_df
    except Exception as e:        
        logger.error(f"Exception in process_incoming_training_data: {e}", exc_info=True)
        raise