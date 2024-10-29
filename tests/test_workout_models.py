
import pytest
from pydantic import ValidationError
from app.models.models import User, TrainingSession, TrainingDetail
from datetime import datetime, timezone
import app.utils.adr_processor as adr
from app.utils.path_utils import get_download_data_path
import pathlib
import pandas as pd

def populate_personal_user_and_session(db):
    # Crear el usuario con alias "personal"
    user = User(
        email="personal@example.com",
        date_of_birth=datetime(1990, 1, 1, tzinfo=timezone.utc),
        gender="Other",
        height=170.0,
        initial_weight=70.0,
        phone_number="1234567890",
        alias="personal"
    )
    
    # Crear la sesión de entrenamiento asociada al usuario
    training_session = TrainingSession(
        user=user,
        date=datetime.now(timezone.utc)
    )
    
    # Añadir ambos a la sesión de la base de datos y confirmar
    db.session.add_all([user, training_session])
    db.session.commit()
    
    return user, training_session

def test_create_user(app,db):
    new_user = User(
    email="my_email@email.com",
    date_of_birth=datetime(1990, 1, 1, tzinfo=datetime.now(timezone.utc).astimezone().tzinfo),
    gender="Other",
    height=175.5,
    initial_weight=70.0,
    phone_number="1234567890"
    )

    db.session.add(new_user)
    db.session.commit()

    user = db.session.get(User, 1)

    assert user == new_user


def test_create_training_detail_from_csv(app,db):
    # Arrange
    user,training_session = populate_personal_user_and_session(db)
    data_path = get_download_data_path()
    file_path = data_path / "adrencoder.csv"
    adr_csv = adr.preprocess_adr_data(file_path)

    # Act
    user_from_csv = adr.get_user_from_df(adr_csv)
    session_from_csv = adr.add_or_return_training_session(user)
    adr.add_dataframe_to_training_detail(adr_csv, user, training_session)

    # Assert
    assert user_from_csv == user
    assert session_from_csv == training_session
    # Verificar que los TrainingDetail se añadieron correctamente
    details = TrainingDetail.query.filter_by(session_id=training_session.id).all()
    assert len(details) == adr_csv.shape[0]

def test_populate_user_and_session(db):
    user, training_session = populate_personal_user_and_session(db)
    assert user.alias.lower() == "personal"
    assert training_session.user_id == user.id


# Add some more info here
def test_preprocess_adr_data():
    data_path = get_download_data_path() / 'adrencoder.csv'
    adr_csv = adr.preprocess_adr_data(data_path)
    assert 'hash_id' in adr_csv.columns
    assert not adr_csv.empty

# Add better checks here (This adds data without being filtered)
def test_add_dataframe_to_training_detail(db):
    user, training_session = populate_personal_user_and_session(db)
    adr_csv = adr.preprocess_adr_data(get_download_data_path() / "adrencoder.csv")
    adr.add_dataframe_to_training_detail(adr_csv, user, training_session)
    details = TrainingDetail.query.filter_by(session_id=training_session.id).all()
    assert len(details) == adr_csv.shape[0]



def test_get_training_df_from_db(db):
    """
    Tests whether the training details added from a CSV match those retrieved from the database.
    
    Args:
        db: The database session fixture.
    """
    # Step 1: Populate user and training session
    user, training_session = populate_personal_user_and_session(db)
    
    # Step 2: Preprocess the ADR CSV data
    adr_csv_path = get_download_data_path() / "adrencoder.csv"
    adr_csv = adr.preprocess_adr_data(adr_csv_path)
    
    # Step 3: Add the processed CSV data to the training detail in the database
    adr.add_dataframe_to_training_detail(adr_csv, user, training_session)
    
    # Step 4: Retrieve the training details from the database as a DataFrame
    db_dataframe = adr.get_training_detail_to_dataframe(user, training_session)
    
    
    # Step 8: Select the relevant columns for comparison
    comparison_columns = [
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
        'ecuacion',
        'hash_id'
    ]
    
    # Step 9: Ensure all comparison columns are present in both DataFrames
    for col in comparison_columns:
        if col not in db_dataframe.columns:
            db_dataframe[col] = pd.NA  # Assign NA for missing columns in raw_df
        if col not in db_dataframe.columns:
            db_dataframe[col] = pd.NA  # Assign NA for missing columns in db_df
    
    # Step 10: Extract only the comparison columns
    raw_selected = adr_csv[comparison_columns].copy()
    db_selected = db_dataframe[comparison_columns].copy()
    
    # Step 11: Sort both DataFrames by 'hash_id' to ensure consistent order
    raw_sorted = raw_selected.sort_values(by='hash_id').reset_index(drop=True)
    db_sorted = db_selected.sort_values(by='hash_id').reset_index(drop=True)
    
    # Step 12: Reset index for both DataFrames to ensure they are aligned
    raw_sorted.reset_index(drop=True, inplace=True)
    db_sorted.reset_index(drop=True, inplace=True)

    # Step 14: Ensure 'timestamp' columns are in datetime format and rounded to microseconds
    raw_sorted = raw_sorted.drop('timestamp', axis=1)
    db_sorted = db_sorted.drop('timestamp', axis=1)
    
    # Step 13: Compare the two DataFrames
    # We'll use pandas.testing.assert_frame_equal for detailed comparison
    try:
        pd.testing.assert_frame_equal(
            raw_sorted,
            db_sorted,
            check_dtype=True,       # Ensure data types are the same
            check_like=False,       # Order matters since we've sorted
            check_exact=True,       # Exact match required
            rtol=1e-5,               # Relative tolerance for floating point comparisons
            atol=1e-8,               # Absolute tolerance
            obj='DataFrame Comparison'
        )
        # If no exception is raised, the DataFrames are equal
        assert True
    except AssertionError as e:
        # If there is an assertion error, the test fails
        pytest.fail(f"DataFrames are not equal:\n{e}")


def test_get_and_filter_from_db(db):
    user, training_session = populate_personal_user_and_session(db)
    adr_csv = adr.preprocess_adr_data(get_download_data_path() / "adrencoder.csv")
    adr_csv_1 = adr.preprocess_adr_data(get_download_data_path() / "adrencoder1.csv")
    adr_filtered = adr.preprocess_adr_data(get_download_data_path() / "adrencoder2.csv") 
    adr.add_dataframe_to_training_detail(adr_csv, user, training_session)
    db_dataframe = adr.get_training_detail_to_dataframe(user, training_session)
    bd_filtered_df = adr.filter_df_based_on_hash(db_dataframe, adr_csv_1)

    
    comparison_columns = [
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
        'ecuacion',
        'hash_id'
    ]

    adr_filtered = adr_filtered[comparison_columns].copy()
    bd_filtered_df = bd_filtered_df[comparison_columns].copy()
    
    # Step 11: Sort both DataFrames by 'hash_id' to ensure consistent order
    raw_sorted = adr_filtered.sort_values(by='hash_id').reset_index(drop=True)
    db_sorted = bd_filtered_df.sort_values(by='hash_id').reset_index(drop=True)
    
    # Step 12: Reset index for both DataFrames to ensure they are aligned
    raw_sorted.reset_index(drop=True, inplace=True)
    db_sorted.reset_index(drop=True, inplace=True)

    # Step 14: Ensure 'timestamp' columns are in datetime format and rounded to microseconds
    raw_sorted = raw_sorted.drop('timestamp', axis=1)
    db_sorted = db_sorted.drop('timestamp', axis=1)
    
    # Step 13: Compare the two DataFrames
    # We'll use pandas.testing.assert_frame_equal for detailed comparison
    try:
        pd.testing.assert_frame_equal(
            raw_sorted,
            db_sorted,
            check_dtype=True,       # Ensure data types are the same
            check_like=False,       # Order matters since we've sorted
            check_exact=True,       # Exact match required
            rtol=1e-5,               # Relative tolerance for floating point comparisons
            atol=1e-8,               # Absolute tolerance
            obj='DataFrame Comparison'
        )
        # If no exception is raised, the DataFrames are equal
        assert True
    except AssertionError as e:
        # If there is an assertion error, the test fails
        pytest.fail(f"DataFrames are not equal:\n{e}")

