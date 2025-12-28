"""
Script untuk memeriksa setup dan troubleshooting
"""
import sys

def check_passlib():
    """Check if passlib is installed"""
    try:
        import passlib
        from passlib.context import CryptContext
        print("✓ passlib installed")
        return True
    except ImportError:
        print("✗ passlib not installed")
        print("  Install dengan: pip install passlib[bcrypt]")
        return False

def check_migration():
    """Check if password column exists in database"""
    try:
        from app.database import SessionLocal, engine
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('workers')]
        
        if 'password' in columns:
            print("✓ password column exists in workers table")
            return True
        else:
            print("✗ password column NOT found in workers table")
            print("  Jalankan migration: python run_migration.py upgrade head")
            return False
    except Exception as e:
        print(f"✗ Error checking database: {str(e)}")
        return False

if __name__ == "__main__":
    print("Checking setup...")
    print("-" * 50)
    
    passlib_ok = check_passlib()
    migration_ok = check_migration()
    
    print("-" * 50)
    if passlib_ok and migration_ok:
        print("✓ All checks passed!")
    else:
        print("✗ Some checks failed. Please fix the issues above.")

