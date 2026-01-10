import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

# Parse DATABASE_URL
# postgresql://massindo:mas5indo@localhost:5432/matrix_massindo
db_url = os.getenv("DATABASE_URL")
# Extract parts (assuming standard format)
# This is a bit hacky but sufficient for this task
user = "massindo"
password = "mas5indo"
host = "localhost"
port = "5432"
dbname = "matrix_massindo"

print(f"Attempting to create database '{dbname}'...")

try:
    # Connect to default 'postgres' database
    con = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database="postgres"
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()
    
    # Check if database exists
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'")
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute(f"CREATE DATABASE {dbname}")
        print(f"Database '{dbname}' created successfully.")
    else:
        print(f"Database '{dbname}' already exists.")
        
    cursor.close()
    con.close()

except Exception as e:
    print(f"Error: {e}")
