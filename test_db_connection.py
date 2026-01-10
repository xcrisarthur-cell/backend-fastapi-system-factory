from app.database import SessionLocal
from app.models import Position, Worker
from sqlalchemy import text

try:
    db = SessionLocal()
    print("Connection successful!")
    
    # Try to query positions
    print("Querying positions...")
    positions = db.query(Position).all()
    print(f"Found {len(positions)} positions")
    
    # Try to query workers
    print("Querying workers...")
    workers = db.query(Worker).all()
    print(f"Found {len(workers)} workers")
    
    db.close()
    print("Test completed successfully.")
except Exception as e:
    print(f"ERROR: {e}")
