import pandas as pd
import psycopg2
from psycopg2 import sql
import os
import glob
from sqlalchemy import create_engine
import sqlalchemy

import config



# killmail_victims
# Index(['character_id', 'corporation_id', 'alliance_id', 'damage_taken',
#        'ship_type_id', 'killmail_id', 'solar_system_id', 'date'],
#       dtype='object')
# killmail_attackers
# Index(['damage_done', 'faction_id', 'final_blow', 'security_status',
#        'ship_type_id', 'killmail_id', 'solar_system_id', 'date', 'alliance_id',
#        'character_id', 'corporation_id', 'weapon_type_id'],
#       dtype='object')
# killmail_items_destroyed
# Index(['killmail_id', 'solar_system_id', 'killmail_time', 'item_type_id',
#        'quantity_destroyed', 'quantity_dropped'],
#       dtype='object')
# killmail_ships_destroyed
# Index(['killmail_id', 'ship_type_id', 'solar_system_id', 'date'], dtype='object')



# Function to create table and insert data
def create_table_killmail_victims(table_name, db_credentials):
    
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
            killmail_id BIGINT NOT NULL,
            character_id BIGINT,
            corporation_id BIGINT,
            alliance_id BIGINT,
            damage_taken BIGINT,
            ship_type_id INTEGER,
            solar_system_id BIGINT
        );
        SELECT create_hypertable('killmail_victims', 'date');
    """).format(sql.Identifier(table_name)))
    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()
    
    
    
def create_table_killmail_attackers(table_name, db_credentials):
    
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
            damage_done INTEGER,
            faction_id INTEGER,
            final_blow BOOLEAN,
            security_status FLOAT,
            ship_type_id INTEGER,
            killmail_id BIGINT,
            solar_system_id INTEGER,
            alliance_id BIGINT,
            character_id BIGINT,
            corporation_id BIGINT,
            weapon_type_id INTEGER
        );
        SELECT create_hypertable('killmail_attackers', 'date');
    """).format(sql.Identifier(table_name)))
    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()
    
    
    
def create_table_killmail_items_destroyed(table_name, db_credentials):
    
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
            killmail_id BIGINT NOT NULL,
            solar_system_id INTEGER,
            killmail_time TIMESTAMP,
            item_type_id INTEGER,
            quantity_destroyed BIGINT,
            quantity_dropped BIGINT
        );
        SELECT create_hypertable('killmail_items_destroyed', 'killmail_time');
    """).format(sql.Identifier(table_name)))
    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()
    
    
    
def create_table_killmail_ships_destroyed(table_name, db_credentials):
    
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
            killmail_id BIGINT NOT NULL,
            ship_type_id INTEGER,
            solar_system_id INTEGER,
            date DATE
        );
        SELECT create_hypertable('killmail_ships_destroyed', 'date');
    """).format(sql.Identifier(table_name)))
    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()