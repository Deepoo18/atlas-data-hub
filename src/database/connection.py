from pathlib import Path
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import execute_batch
from src.utils.logger import log

load_dotenv(override=True)


def get_connection():
    """
    Establishes a connection to the PostgreSQL database using psycopg2.

    Returns:
        connection: A psycopg2 connection object.
    """
    try:
        # Replace these values with your actual database credentials
        connection = psycopg2.connect(
            host=os.getenv("host"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password")
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


def load_data_to_db(data, table_name):
    conn = get_connection()
    cursor = conn.cursor()
    logger = log()

    columns = data[0].keys()
    column_name = ",".join(columns)
    placeholders =", ".join(f"%({column})s" for column in columns)

    insert_query = f"""
    INSERT INTO {table_name} ({column_name}) VALUES ({placeholders})
    """
    try:
        execute_batch(cursor, insert_query, data,page_size=100)
        print(f"Inserted {len(data)} records into {table_name} successfully.")
        logger.info(f"Inserted {len(data)} records into {table_name} successfully.")
    except Exception as e:
        logger.error(f"Error inserting data into {table_name}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
