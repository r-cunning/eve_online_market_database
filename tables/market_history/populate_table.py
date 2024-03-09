import os
import pandas as pd
import bz2
import glob
from sqlalchemy import create_engine

def populate_market_table(csv_folder_path, db_credentials):
    """
    Load CSV files from a specified folder into a TimescaleDB table.

    Args:
        csv_folder_path (str): The path to the folder containing the CSV files.
        db_credentials (dict): A dictionary containing the credentials for connecting to the PostgreSQL database.
            The dictionary should have the following keys: 'user', 'password', 'host', 'port', 'dbname'.

    Returns:
        None
    """
    
    print('Creating engine...')
    
    # Create a connection to the PostgreSQL database
    engine = create_engine(f'postgresql+psycopg2://{db_credentials["user"]}:{db_credentials["password"]}@{db_credentials["host"]}:{db_credentials["port"]}/{db_credentials["dbname"]}')

    # Use glob to find all .csv.bz2 files, including subdirectories
    print('Finding files...')
    for root, dirs, files in os.walk(csv_folder_path):
        for file in files:
            if file.endswith('.csv'):
                csv_file_path = os.path.join(root, file)
                print(f"Processing {csv_file_path}...")

                
                df = pd.read_csv(csv_file_path, usecols=['date', 'region_id', 'type_id',
                                                'average', 'lowest', 'highest', 'volume', 'order_count'])

                # Insert DataFrame into database table
                df.to_sql('market_history', engine, if_exists='append', index=False, method='multi')
                print(f"Loaded {csv_file_path} into database.")

    # Close the database connection
    engine.dispose()