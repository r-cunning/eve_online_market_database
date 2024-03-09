import pandas as pd
from sqlalchemy import create_engine





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
    engine = create_engine(f'postgresql+psycopg2://{db_credentials["user"]}:{db_credentials["password"]}@{db_credentials["host"]}:{db_credentials["port"]}/{db_credentials["dbname"]}')

    
    
    
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
