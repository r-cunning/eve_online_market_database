import pandas as pd
import psycopg2
from psycopg2 import sql
import os
import glob
from sqlalchemy import create_engine
import sqlalchemy

import config





# Function to create table and insert data
def create_table(table_name, db_credentials):
    # Connect to the PostgreSQL database
    print("Connecting to database")
    conn = psycopg2.connect(dbname=db_credentials['dbname'], user=db_credentials['user'], 
                            password=db_credentials['password'], host=db_credentials['host'], 
                            port=db_credentials['port'])
    cur = conn.cursor()
    print("Connected to database")
    # Create table if it doesn't exist
    cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {}
        (
            date DATE NOT NULL,
            faction_id INTEGER NOT NULL,
            pilots INTEGER,
            systems_controlled INTEGER,
            kills_last_week INTEGER,
            kills_total INTEGER,
            kills_yesterday INTEGER,
            victory_points_last_week INTEGER,
            victory_points_total INTEGER,
            victory_points_yesterday INTEGER
        );
        SELECT create_hypertable('faction_warfare_stats_history', 'date');
    """).format(sql.Identifier(table_name)))
    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()