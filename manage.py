#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from urllib.parse import urlparse
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv
from alembic.config import Config
from alembic.script import ScriptDirectory

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_corrected_db_url(url):
    """
    Ensure the URL scheme is postgresql:// for SQLAlchemy
    """
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url

def get_postgres_url(url):
    """
    Returns the connection URL for the default 'postgres' database,
    derived from the given DATABASE_URL.
    """
    parsed = urlparse(url)
    scheme = parsed.scheme
    if scheme == 'postgres':
        scheme = 'postgresql'
        
    return f"{scheme}://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port}/postgres"

def get_db_name(url):
    parsed = urlparse(url)
    return parsed.path.lstrip('/')

def check_and_create_database():
    print("Checking database...")
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found in environment.")
        sys.exit(1)

    db_name = get_db_name(DATABASE_URL)
    postgres_url = get_postgres_url(DATABASE_URL)

    try:
        # Connect to default 'postgres' database to check/create target DB
        engine = create_engine(postgres_url, isolation_level="AUTOCOMMIT")
        with engine.connect() as conn:
            # Check if database exists
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
            exists = result.scalar()

            if not exists:
                print(f"Database '{db_name}' does not exist. Creating...")
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"Database '{db_name}' created successfully.")
            else:
                print(f"Database '{db_name}' already exists.")
    except Exception as e:
        print(f"Error checking/creating database: {e}")
        # Don't exit here, maybe the user doesn't have access to 'postgres' db 
        # but the target db might already work. 
        # But for now, let's keep it safe.
        sys.exit(1)

def get_alembic_cmd():
    bin_dir = os.path.dirname(sys.executable)
    alembic_cmd = os.path.join(bin_dir, "alembic")
    if os.path.exists(alembic_cmd):
        return alembic_cmd
    return "alembic"

def run_migrations():
    print("Checking migration status...")
    
    target_url = get_corrected_db_url(DATABASE_URL)
    alembic_cmd = get_alembic_cmd()
    
    try:
        engine = create_engine(target_url)
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        has_divisions = 'divisions' in existing_tables
        has_alembic = 'alembic_version' in existing_tables
        
        should_stamp = False
        
        if has_divisions:
            if not has_alembic:
                print("Detected existing tables but no migration history. Stamping head...")
                should_stamp = True
            else:
                with engine.connect() as conn:
                    try:
                        version = conn.execute(text("SELECT version_num FROM alembic_version")).scalar()
                        if not version:
                            print("Detected existing tables but empty migration history. Stamping head...")
                            should_stamp = True
                    except Exception:
                        should_stamp = True
        
        if should_stamp:
            print("Performing manual stamp...")
            try:
                alembic_cfg = Config("alembic.ini")
                script = ScriptDirectory.from_config(alembic_cfg)
                head_revision = script.get_current_head()
                
                print(f"Manual stamping to revision: {head_revision}")
                
                with engine.begin() as conn:
                    if not has_alembic:
                        conn.execute(text("""
                            CREATE TABLE IF NOT EXISTS alembic_version (
                                version_num VARCHAR(32) NOT NULL, 
                                CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
                            )
                        """))
                    
                    conn.execute(text("DELETE FROM alembic_version"))
                    conn.execute(text("INSERT INTO alembic_version (version_num) VALUES (:rev)"), {"rev": head_revision})
                
                print("Database successfully manually stamped.")
            except Exception as e:
                print(f"Manual stamp failed: {e}")
                sys.exit(1)

        print("Running migrations (upgrade head)...")
        # Run alembic upgrade head
        result = subprocess.run([alembic_cmd, "upgrade", "head"], check=True)
        if result.returncode == 0:
            print("Migrations applied successfully.")
        else:
            print("Migration failed.")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: '{alembic_cmd}' command not found. Make sure it is installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Error checking migration state: {e}")
        sys.exit(1)

def run_seeder():
    print("Running seeder...")
    try:
        # Run seeder.py
        result = subprocess.run([sys.executable, "seeder.py"], check=True)
        if result.returncode == 0:
            print("Seeding completed successfully.")
        else:
            print("Seeding failed.")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running seeder: {e}")
        sys.exit(1)

def main():
    print("Starting environment setup...")
    check_and_create_database()
    run_migrations()
    run_seeder()
    print("Environment setup completed successfully.")

if __name__ == "__main__":
    main()
