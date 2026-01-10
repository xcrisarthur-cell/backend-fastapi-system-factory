import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

dbname = "matrix_massindo"
user_to_create = "massindo"
pass_to_create = "mas5indo"

# List of potential passwords for 'postgres' user
passwords = ["postgres", "admin", "123456", "password", ""]

for password in passwords:
    print(f"Trying to connect as 'postgres' with password '{password}'...")
    try:
        con = psycopg2.connect(
            user="postgres",
            password=password,
            host="localhost",
            port="5432",
            database="postgres"
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        print("Success! Connected as 'postgres'.")
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database '{dbname}'...")
            cursor.execute(f"CREATE DATABASE {dbname} OWNER {user_to_create}")
            print(f"Database '{dbname}' created successfully.")
        else:
            print(f"Database '{dbname}' already exists.")
            
        cursor.close()
        con.close()
        break
    except Exception as e:
        print(f"Failed: {e}")
