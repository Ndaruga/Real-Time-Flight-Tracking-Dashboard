import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError
import time

load_dotenv()

DATABASE_NAME = "World_airports"

def connect_to_database():
    try:
        conn = psycopg2.connect(
            database=DATABASE_NAME,
            user="frank",
            password=os.environ.get("POSTGRES_PASSWORD"),
            host=os.environ.get("POSTGRES_HOST"),
            port=os.environ.get("POSTGRES_PORT")
        )
        conn.autocommit = True
        return conn
    except OperationalError as e:
        if "database \"%s\" does not exist" % DATABASE_NAME in str(e):
            return None
        else:
            raise e

# Connect to default database to create user role and drop/recreate the target database
conn_default = psycopg2.connect(
    database="postgres",
    user="postgres",  # Connect with the default user
    password=os.environ.get("POSTGRES_PASSWORD"),
    host=os.environ.get("POSTGRES_HOST"),
    port=os.environ.get("POSTGRES_PORT")
)
conn_default.autocommit = True
cursor_default = conn_default.cursor()

# Drop existing database, if any, and create a new one
cursor_default.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME}")
cursor_default.execute("CREATE ROLE frank WITH LOGIN PASSWORD %s", (os.environ.get("POSTGRES_PASSWORD"),))
cursor_default.execute(f"CREATE DATABASE {DATABASE_NAME} OWNER frank")
cursor_default.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DATABASE_NAME} TO frank")
print("Database created.")

# Close connection to default database
conn_default.close()

# Retry connection until it succeeds or the maximum number of retries is reached
max_retries = 10
retry_delay = 2  # Delay in seconds between retries
retries = 0

while retries < max_retries:
    conn_db = connect_to_database()
    if conn_db:
        break
    else:
        print(f"Database '{DATABASE_NAME}' not yet available. Retrying in {retry_delay} seconds...")
        retries += 1
        time.sleep(retry_delay)

if retries == max_retries:
    print(f"Failed to connect to database '{DATABASE_NAME}' after {max_retries} retries. Exiting...")
    exit()

# Connect to the newly created database
conn_db = connect_to_database()
cursor_db = conn_db.cursor()

# Read CSV files and upload to PostgreSQL
for filename in os.listdir("./data"):
    if filename.endswith(".csv"):
        table_name = os.path.splitext(filename)[0]  # Extract table name from filename
        with open(f"data/{filename}", 'r') as f:
            next(f)  # Skip the header
            cursor_db.copy_from(f, table_name, sep=',')
            print(f"Data loaded into {table_name}.")

# Close connection to the database
conn_db.close()
