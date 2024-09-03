

import psycopg2
from psycopg2 import sql
import pandas as pd

def get_static_data(config, table_name):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(dbname=config.dbname, user=config.user, password=config.password, host=config.host, port=config.port)
    cur = conn.cursor()
    
    # Execute the query to fetch all data from the table and load it into a DataFrame
    query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
    cur.execute(query)
    data = pd.read_sql_query(query, conn)

    # Close the cursor and the connection
    cur.close()
    conn.close()

    # Return the DataFrame containing the data from the table
    return data
