import pandas as pd
from sqlalchemy import create_engine
import psycopg2 
from psycopg2 import sql

def get_latest_date(db_credentials):
    # SQL query to get the latest date in the market_history table
    query = "SELECT MAX(date) AS latest_date FROM market_history"
    
    # SQLAlchemy engine for Pandas
    engine = create_engine(f'postgresql+psycopg2://{db_credentials["user"]}:{db_credentials["password"]}@{db_credentials["host"]}:{db_credentials["port"]}/{db_credentials["dbname"]}')

    try:
        # Use Pandas to execute the query and fetch the result
        result = pd.read_sql(query, engine)
        # Extract the date from the result
        date = result.iloc[0]['latest_date']
        return date

    except Exception as e:
        print(f"An error occurred: {e}")
        return None




def get_market_history(config, table_name, type_id, region_id, start_date, end_date):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(dbname=config.dbname, user=config.user, password=config.password, host=config.host, port=config.port)
    cur = conn.cursor()
    
    # SQL query with type_id, region_id, and date filtering
    query = sql.SQL("SELECT * FROM {} WHERE type_id = %s AND region_id = %s AND date >= %s AND date <= %s").format(sql.Identifier(table_name))
    
    # Execute the query with parameters for type_id, region_id, start_date, and end_date
    cur.execute(query, (type_id, region_id, start_date, end_date))
    
    # Load the query results into a DataFrame using pandas
    df = pd.read_sql_query(query.as_string(conn), conn, params=(type_id, region_id, start_date, end_date))
    
    # Close the cursor and the connection
    cur.close()
    conn.close()
    
    # Return the DataFrame containing the data from the table
    return df
