import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine
from psycopg2 import OperationalError
import time

load_dotenv()

DATABASE_NAME = "World_airports"


# Connect to default database to create user role and drop/recreate the target database
conn_default = psycopg2.connect(
    database=os.environ.get("POSTGRES_DEFAULT_DATABASE"),
    user=os.environ.get("DEFAULT_USER"),  # Connect with the default user
    password=os.environ.get("DEFAULT_USER_PASSWORD"),
    host=os.environ.get("POSTGRES_HOST"),
    port=os.environ.get("POSTGRES_PORT")
)
conn_default.autocommit = True
cursor_default = conn_default.cursor()

# Drop existing database, if any, and create a new one
cursor_default.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME.lower()}")

try:
    cursor_default.execute(f"CREATE ROLE {os.environ.get("POSTGRES_USER")} WITH LOGIN PASSWORD %s", (os.environ.get("POSTGRES_PASSWORD"),))
except psycopg2.errors.DuplicateObject as e:
    print(f"User Role '{os.environ.get("POSTGRES_USER")}' already exists. Skipping role creation...")

cursor_default.execute(f"CREATE DATABASE {DATABASE_NAME.lower()} OWNER {os.environ.get("POSTGRES_USER")}")
cursor_default.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DATABASE_NAME.lower()} TO frank")
print(f"{DATABASE_NAME} Database created.\n")

# Close connection to default database
conn_default.close()


# CONNECT TO THE NEWLY CREATED DATABASE
try:
    conn_string = f'postgresql://{os.environ.get("POSTGRES_USER")}:{os.environ.get("POSTGRES_PASSWORD")}@{os.environ.get("POSTGRES_HOST")}/{DATABASE_NAME.lower()}'
    print(f"Connected to {DATABASE_NAME.lower()} database...\n")
except OperationalError as e:
    if "database \"%s\" does not exist" % DATABASE_NAME in str(e):
        print(f"Database '{DATABASE_NAME}' does not exist on this server.")
    else:
        print(f"Error connecting to database '{DATABASE_NAME}': {e}")

db = create_engine(conn_string) 
conn = db.connect()


# Read CSV files and upload to PostgreSQL
for filename in os.listdir("./data"):
    if filename.endswith(".csv"):
        data= pd.read_csv(f"data/{filename}")
        table_name = filename.split(".")[0]
        # converting data to sql 
        data.to_sql(table_name, conn, if_exists= 'replace')
        print(f"Data loaded into '{table_name}' table.")

# Close connection to the database
conn.close()
