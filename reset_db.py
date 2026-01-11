import psycopg2
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
    match = re.match(r"postgresql://([^:]+):([^@]+)@([^:/]+)(?::(\d+))?/([^?]+)", db_url)
    
    if not match:
        print(f"Could not parse DATABASE_URL: {db_url}")
        sys.exit(1)

    user, password, host, port, dbname = match.groups()
    if not port:
        port = "5432"

    print(f"Connecting to database '{dbname}' to drop all tables...")

    try:
        # Connect to the target database directly
        con = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=dbname
        )
        con.autocommit = True
        cursor = con.cursor()

        print("Dropping all tables in public schema...")
        cursor.execute("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                -- Drop tables
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS "public"."' || r.tablename || '" CASCADE';
                END LOOP;
            END $$;
        """)
        
        print("Dropping all types/enums in public schema...")
        cursor.execute("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                -- Drop enums/types
                FOR r IN (
                    SELECT t.typname 
                    FROM pg_type t 
                    JOIN pg_namespace n ON t.typnamespace = n.oid 
                    WHERE n.nspname = 'public' 
                    AND t.typtype = 'e'
                ) LOOP
                    EXECUTE 'DROP TYPE IF EXISTS "public"."' || r.typname || '" CASCADE';
                END LOOP;
            END $$;
        """)

        cursor.close()
        con.close()
        print("Database reset successfully (all tables dropped).")

    except Exception as e:
        print(f"Error resetting database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    reset_database()
