import pandas as pd
import psycopg2
from psycopg2 import sql
import os
import glob
from sqlalchemy import create_engine
import sqlalchemy

import config





# Function to create table and insert data
def create_table(db_credentials, table_name):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_credentials)
    cur = conn.cursor()
    print("Check 2")
    # Create table if it doesn't exist
    cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {}
    (
        date DATE NOT NULL,
        region_id INTEGER NOT NULL,
        type_id INTEGER NOT NULL,
        average BIGINT NOT NULL,
        highest BIGINT NOT NULL,
        lowest BIGINT NOT NULL,
        volume BIGINT NOT NULL,
        order_count BIGINT NOT NULL
    );
    """).format(sql.Identifier(table_name)))
    
    cur.execute(sql.SQL("SELECT create_hypertable(%s, 'date');"), (table_name,))

    
    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()
