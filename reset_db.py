import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import re
import sys
from dotenv import load_dotenv

load_dotenv()

def reset_database():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not found in .env")
        sys.exit(1)

    # Simple regex to parse postgres url
    # postgresql://user:pass@host:port/dbname
    # Handle optional port
    match = re.match(r"postgresql://([^:]+):([^@]+)@([^:/]+)(?::(\d+))?/([^?]+)", db_url)
    
    if not match:
        print(f"Could not parse DATABASE_URL: {db_url}")
        sys.exit(1)

    user, password, host, port, dbname = match.groups()
    if not port:
        port = "5432"

    print(f"Connecting to postgres to reset '{dbname}'...")

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

        # Kill existing connections
        print(f"Terminating existing connections to {dbname}...")
        cursor.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{dbname}'
            AND pid <> pg_backend_pid();
        """)

        # Drop database
        print(f"Dropping database {dbname}...")
        cursor.execute(f"DROP DATABASE IF EXISTS {dbname}")

        # Create database
        print(f"Creating database {dbname}...")
        cursor.execute(f"CREATE DATABASE {dbname}")

        cursor.close()
        con.close()
        print("Database reset successfully.")

    except Exception as e:
        print(f"Error resetting database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    reset_database()
