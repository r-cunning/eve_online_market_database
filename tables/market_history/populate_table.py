import os
import pandas as pd
import bz2
import glob
from sqlalchemy import create_engine
from datetime import datetime

def populate_market_table(csv_folder_path, db_credentials, start_date=None):
    """
    Load CSV files from a specified folder into a TimescaleDB table, starting from a specified date.
    Files are pre-filtered based on their names which include dates.

    Args:
        csv_folder_path (str): The path to the folder containing the CSV files.
        db_credentials (dict): A dictionary containing the credentials for connecting to the PostgreSQL database.
            The dictionary should have the following keys: 'user', 'password', 'host', 'port', 'dbname'.
        start_date (str): The earliest date from which to begin loading data (inclusive), in YYYY-MM-DD format.

    Returns:
        None
    """
    
    print('Creating engine...')
    
    # Create a connection to the PostgreSQL database
    engine = create_engine(f'postgresql+psycopg2://{db_credentials["user"]}:{db_credentials["password"]}@{db_credentials["host"]}:{db_credentials["port"]}/{db_credentials["dbname"]}')

    # Convert start_date to datetime for comparison
    if start_date is not None:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')

    print('Finding files...')
    for root, dirs, files in os.walk(csv_folder_path):
        for file in files:
            if file.endswith('.csv'):
                # Extract the date from the filename
                date_str = file.split('-')[2:5]  # Assumes format 'market-history-YYYY-MM-DD.csv'
                file_date = datetime.strptime('-'.join(date_str), '%Y-%m-%d.csv')

                if start_date is None or file_date >= start_date:
                    csv_file_path = os.path.join(root, file)
                    print(f"Processing {csv_file_path}...")

                    # Load the CSV file into a DataFrame
                    df = pd.read_csv(csv_file_path, usecols=['date', 'region_id', 'type_id', 'average', 'lowest', 'highest', 'volume', 'order_count'])

                    # Insert DataFrame into database table
                    df.to_sql('market_history', engine, if_exists='append', index=False, method='multi')
                    print(f"Loaded {csv_file_path} into database.")
                else:
                    print(f"Skipped {file} as it is before the start date {start_date}.")

    # Close the database connection
    engine.dispose()





# def populate_market_table(csv_folder_path, db_credentials):
#     """
#     Load CSV files from a specified folder into a TimescaleDB table.

#     Args:
#         csv_folder_path (str): The path to the folder containing the CSV files.
#         db_credentials (dict): A dictionary containing the credentials for connecting to the PostgreSQL database.
#             The dictionary should have the following keys: 'user', 'password', 'host', 'port', 'dbname'.

#     Returns:
#         None
#     """
    
#     print('Creating engine...')
    
#     # Create a connection to the PostgreSQL database
#     engine = create_engine(f'postgresql+psycopg2://{db_credentials["user"]}:{db_credentials["password"]}@{db_credentials["host"]}:{db_credentials["port"]}/{db_credentials["dbname"]}')

#     # Use glob to find all .csv.bz2 files, including subdirectories
#     print('Finding files...')
#     for root, dirs, files in os.walk(csv_folder_path):
#         for file in files:
#             if file.endswith('.csv'):
#                 csv_file_path = os.path.join(root, file)
#                 print(f"Processing {csv_file_path}...")

                
#                 df = pd.read_csv(csv_file_path, usecols=['date', 'region_id', 'type_id',
#                                                 'average', 'lowest', 'highest', 'volume', 'order_count'])

#                 # Insert DataFrame into database table
#                 df.to_sql('market_history', engine, if_exists='append', index=False, method='multi')
#                 print(f"Loaded {csv_file_path} into database.")

#     # Close the database connection
#     engine.dispose()