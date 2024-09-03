import os
import json
import pandas as pd
import tarfile
import psycopg2
from sqlalchemy import create_engine, Column, Integer, Float, String, Date, BigInteger, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()



def process_tar_bz2_file(file_path, db_connection_string):
    victims_data = []
    attackers_data = []
    items_data = []
    ships_destroyed_data = []

    victim_categories = ['character_id', 'corporation_id', 'alliance_id', 'damage_taken', 'ship_type_id']

    with tarfile.open(file_path, 'r:bz2') as tar:
        for member in tar.getmembers():
            f = tar.extractfile(member)
            if f is not None:
                data = json.load(f)
                
                # print("Data Loaded", member)
                
                killmail_id = data['killmail_id']
                solar_system_id = data['solar_system_id']
                killmail_time = data['killmail_time']

                # Process victim data
                victim_data = {key: data['victim'][key] for key in victim_categories if key in data['victim']}
                victim_data.update({'killmail_id': killmail_id, 'solar_system_id': solar_system_id, 'date': killmail_time})
                victims_data.append(victim_data)

                # Process attacker data
                for attacker in data['attackers']:
                    attacker.update({'killmail_id': killmail_id, 'solar_system_id': solar_system_id, 'date': killmail_time})
                    attackers_data.append(attacker)

                
                # Process items data
                for item in data['victim'].get('items', []):
                    # Extracting only relevant item data and skipping any nested structures
                    item_data = {
                        'killmail_id': killmail_id,
                        'solar_system_id': solar_system_id,
                        'killmail_time': killmail_time,
                        'item_type_id': item.get('item_type_id'),
                        'quantity_destroyed': item.get('quantity_destroyed'),
                        'quantity_dropped': item.get('quantity_dropped')
                    }
                    items_data.append(item_data)

                # Add to ships_destroyed dataframe
                ships_destroyed_data.append({'killmail_id': killmail_id, 'ship_type_id': victim_data['ship_type_id'], 
                                             'solar_system_id': solar_system_id, 'date': killmail_time})
                
                
                

    # # Convert lists to DataFrames
    victims_df = pd.DataFrame(victims_data)
    attackers_df = pd.DataFrame(attackers_data)
    items_df = pd.DataFrame(items_data)
    ships_destroyed_df = pd.DataFrame(ships_destroyed_data)
    # print(items_df.head())
    
    # print('killmail_victims')
    # print(victims_df.columns)
    
    # print('killmail_attackers')
    # print(attackers_df.columns)
    
    # print('killmail_items_destroyed')
    # print(items_df.columns)
    
    # print('killmail_ships_destroyed')
    # print(ships_destroyed_df.columns)

    # Create SQLAlchemy engine and session
    engine = create_engine(db_connection_string)
    Base.metadata.create_all(engine)

    
    pd.DataFrame(victims_df).to_sql('killmail_victims', engine, if_exists='append', index=False)
    pd.DataFrame(attackers_df).to_sql('killmail_attackers', engine, if_exists='append', index=False)
    pd.DataFrame(items_df).to_sql('killmail_items_destroyed', engine, if_exists='append', index=False)
    pd.DataFrame(ships_destroyed_df).to_sql('killmail_ships_destroyed', engine, if_exists='append', index=False)

def ingest_tar_bz2_json_files(directory, db_credentials):
    db_connection_string = f"postgresql+psycopg2://{db_credentials['user']}:{db_credentials['password']}@{db_credentials['host']}:{db_credentials['port']}/{db_credentials['dbname']}"
    
    # print("Function Called", directory)
    for root, dirs, files in os.walk(directory):
    
        # print("Processing directory:", str(dirs))
        for file in files:
            # print("Processing file:", file)
            if file.endswith('.bz2'):
                file_path = os.path.join(root, file)
                # print("Processing file:", file_path)
                process_tar_bz2_file(file_path, db_connection_string)


import os
import datetime

import os
import datetime

def start_date_ingest_tar_bz2_json_files(directory, db_credentials, start_date_str):
    # Parse start date string into datetime object
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
    
    # Build the database connection string
    db_connection_string = f"postgresql+psycopg2://{db_credentials['user']}:{db_credentials['password']}@{db_credentials['host']}:{db_credentials['port']}/{db_credentials['dbname']}"
    
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if file ends with .bz2 and has the correct date format in the name
            if file.endswith('.bz2') and 'killmails' in file:
                try:
                    # Extract date from the filename assuming the format 'killmails-YYYY-MM-DD.tar.bz2'
                    date_part = file.split('-')[1:4]  # This should capture ['YYYY', 'MMDD']    
                    date_part[2] = date_part[2].split('.tar.bz2')[0]
                    
                        
                    year = date_part[0]
                    month = date_part[1]
                    day = date_part[2]
                    file_date_str = f"{year}-{month}-{day}"
                    print(file_date_str)
                    file_date = datetime.datetime.strptime(file_date_str, '%Y-%m-%d')
                    
                    # Process files on or after the start date
                    if file_date >= start_date:
                        file_path = os.path.join(root, file)
                        process_tar_bz2_file(file_path, db_connection_string)
                except ValueError as e:
                    print(f"Error processing file {file}: {str(e)}")


