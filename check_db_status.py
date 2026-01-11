import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

load_dotenv()

url = os.getenv("DATABASE_URL")
print(f"DATABASE_URL from env: {url}")

if url:
    engine = create_engine(url)
    try:
        with engine.connect() as conn:
            print("Connected successfully.")
            # Check tables
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"Tables in DB: {tables}")
            
            # Check alembic version
            try:
                result = conn.execute(text("SELECT * FROM alembic_version"))
                print(f"Alembic version: {result.fetchall()}")
            except Exception as e:
                print(f"Could not read alembic_version: {e}")
                
    except Exception as e:
        print(f"Connection failed: {e}")
else:
    print("No DATABASE_URL found.")
