import psycopg2
import pandas as pd
from database.db_config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def create_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, 
            user=DB_USER, 
            password=DB_PASSWORD, 
            host=DB_HOST, 
            port=DB_PORT
        )
    except psycopg2.DatabaseError as e:
        print(f"Error: {e}")
        raise e
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS TRADE_HISTORY (
        Date_UTC_IN TIMESTAMP,
        Date_UTC_OUT TIMESTAMP,
        Trade_Duration INTERVAL,
        Symbol_IN TEXT,
        Position TEXT,
        Price_IN REAL,
        Price_OUT REAL,
        Percentage REAL,
        Quantity_IN REAL,
        Amount_IN REAL,
        Amount_OUT REAL,
        Fee_IN REAL,
        Fee_OUT REAL,
        Total_Fee REAL,
        Realized_Profit REAL,
        Earning REAL,
        Total_Money REAL,
        leverage REAL
    );
    """

    try:
        cursor.execute(create_table_sql)
        conn.commit()
    except psycopg2.DatabaseError as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def insert_data(data_tuples, table_name, columns):
    
    conn = create_connection()
    cursor = conn.cursor()

    # Prepare the SQL insert statement
    placeholders = ', '.join(['%s'] * len(columns))
    column_names = ', '.join(columns)
    insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

    try:
        cursor.executemany(insert_query, data_tuples)
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def fetch_data():
    conn = create_connection()
    try:
        query = "SELECT * FROM TRADE_HISTORY;"  # Adjust the query as needed
        df = pd.read_sql_query(query, conn)
        return df
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return pd.DataFrame()
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    input_path = './data/raw/Export Trade History_2.xlsx'
    output_folder = './data/processed'
    file_pattern = "Processed_Trade_History_*.csv"
    table_name = 'TRADE_HISTORY'
    df= fetch_data()
    table_name = 'TRADE_HISTORY'



