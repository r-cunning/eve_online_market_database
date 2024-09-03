import pandas as pd
from sqlalchemy import create_engine
import psycopg2 
from psycopg2 import sql


def get_FW_history(config, table_name, start_date, end_date):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(dbname=config.dbname, user=config.user, password=config.password, host=config.host, port=config.port)
    cur = conn.cursor()
    
    # SQL query with type_id, region_id, and date filtering
    query = sql.SQL("SELECT * FROM {} WHERE date >= %s AND date <= %s").format(sql.Identifier(table_name))
    
    # Execute the query with parameters for type_id, region_id, start_date, and end_date
    cur.execute(query, (start_date, end_date))
    
    # Load the query results into a DataFrame using pandas
    df = pd.read_sql_query(query.as_string(conn), conn, params=(start_date, end_date))
    
    # Close the cursor and the connection
    cur.close()
    conn.close()
    
    # Return the DataFrame containing the data from the table
    return df





def get_history(db_credentials, faction_id = None, start_date=None, end_date=None):
   
    params = []
   
    # SQL query
    if faction_id is not None:
        query = """
        SELECT * FROM faction_warfare_stats_history WHERE faction_id = %s
        """
        params.append(faction_id)
    else:
        query = """
        SELECT * FROM faction_warfare_stats_history
        """
        
    # Add date range conditions to the query if start_date and end_date are specified
    if start_date is not None and end_date is not None:
        query += " AND date >= %s AND date <= %s"
        params.append(start_date)
        params.append(end_date)
        
    # SQLAlchemy engine for Pandas
    engine = create_engine(f'postgresql+psycopg2://{db_credentials.user}:{db_credentials.password}@{db_credentials.host}:{db_credentials.port}/{db_credentials.dbname}')

    
    
    
    # # Use Pandas to load the query results into a DataFrame
    try:
    #     if start_date is not None and end_date is not None:
        df = pd.read_sql(query, engine, params=params)
    #         if faction_id is not None:
    #             df = pd.read_sql(query, engine, params=(faction_id, start_date, end_date))
    #         else:
    #             df = pd.read_sql(query, engine, params=(start_date, end_date))
    #     else:
    #         if faction_id is not None:
    #             df = pd.read_sql(query, engine, params=(faction_id))
    #         else:
    #             df = pd.read_sql(query, engine)
        
        # Convert 'date' column to datetime and sort by date
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date')
        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
