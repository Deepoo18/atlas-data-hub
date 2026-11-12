import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


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