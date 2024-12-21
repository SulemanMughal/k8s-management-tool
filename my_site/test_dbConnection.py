# import os
import psycopg2
from psycopg2 import OperationalError
from decouple import config, Csv

def create_connection():
    # Reading connection parameters from environment variables
    db_name = config("DB_NAME")
    db_user = config("DB_USER")
    db_password = config("DB_PASSWORD")
    db_host = config("DB_HOST")
    db_port = config("DB_PORT")  # Default to port 5432 if not set

    try:
        # Establish the connection
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("Connection to PostgreSQL DB successful")
        return connection

    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None

def close_connection(connection):
    if connection:
        connection.close()
        print("Connection closed")

if __name__ == "__main__":
    conn = create_connection()
    # Your logic here (e.g., executing queries, etc.)
    close_connection(conn)

