import pandas as pd
from sqlalchemy import create_engine





def get_ships_history(ship_type_id, db_credentials, start_date=None, end_date=None):
    # SQL query
    query = """
    SELECT * FROM killmail_ships_destroyed WHERE ship_type_id = %s
    """

    # Add date range conditions to the query if start_date and end_date are specified
    if start_date is not None and end_date is not None:
        query += " AND date >= %s AND date <= %s"

    # SQLAlchemy engine for Pandas
    engine = create_engine(f'postgresql+psycopg2://{db_credentials["user"]}:{db_credentials["password"]}@{db_credentials["host"]}:{db_credentials["port"]}/{db_credentials["dbname"]}')

    # Use Pandas to load the query results into a DataFrame
    try:
        if start_date is not None and end_date is not None:
            df = pd.read_sql(query, engine, params=(ship_type_id, start_date, end_date))
        else:
            df = pd.read_sql(query, engine, params=(ship_type_id,))
        
        # Convert 'date' column to datetime and sort by date, ensuring timezone-aware datetimes are handled
        df['date'] = pd.to_datetime(df['date'], utc=True)  # Ensure timezone-aware datetimes are handled correctly
        df = df.sort_values(by='date')
        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

