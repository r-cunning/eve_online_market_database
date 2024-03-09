import os
import pandas as pd
from pandas import json_normalize

import bz2
import glob
from sqlalchemy import create_engine
from datetime import datetime
import json


def process_json_populate_FW(base_path, db_credentials):
    # Insert DataFrame into database table
    engine = create_engine(f'postgresql+psycopg2://{db_credentials["user"]}:{db_credentials["password"]}@{db_credentials["host"]}:{db_credentials["port"]}/{db_credentials["dbname"]}')
    for year_folder in os.listdir(base_path):  # Loop through each year
        year_data = []
        year_path = os.path.join(base_path, year_folder)
        if not os.path.isdir(year_path):  # Skip if it's not a directory
            continue

        for day_folder in os.listdir(year_path):  # Loop through each day in the year
            day_path = os.path.join(year_path, day_folder)
            if not os.path.isdir(day_path):  # Skip if it's not a directory
                continue

            # Optionally, validate and convert day_folder to a date object here
            # This example assumes day_folder is in the format YYYY-MM-DD
            try:
                date = datetime.strptime(day_folder, '%Y-%m-%d').date()
            except ValueError:
                # Skip or handle folders not matching the expected date format
                print(f"Skipping {day_folder}: does not match expected date format.")
                continue

            for file_name in os.listdir(day_path):  # Loop through each file in the day folder
                if file_name.endswith('.json.bz2'):  # Check if it's a .json.bz2 file
                    file_path = os.path.join(day_path, file_name)

                    # Extract JSON content from .bz2 file
                    with bz2.open(file_path, 'rt') as bz_file:
                        data = json.load(bz_file)  # Load JSON content

                        # Use json_normalize to flatten the nested structures
                        df = json_normalize(data)
                        df['date'] = date  # Add the date column to the DataFrame
                        
                        for col in df.columns:
                            if col.__contains__('.'):
                                df.rename(columns={col: col.replace('.', '_')}, inplace=True)
                        
                        year_data.append(df)
        # Concatenate all DataFrames in the list into a single DataFrame
        final_df = pd.concat(year_data, ignore_index=True)
        print(final_df.columns)
        final_df.to_sql('faction_warfare_stats_history', engine, if_exists='append', index=False, method='multi')
    return final_df
