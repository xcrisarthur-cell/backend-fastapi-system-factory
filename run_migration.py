"""
Helper script untuk menjalankan migration
"""
import subprocess
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def run_migration(command="upgrade head"):
    """Run alembic migration"""
    print(f"Running: alembic {command}")
    result = subprocess.run(
        ["alembic", *command.split()],
        cwd=os.path.dirname(__file__)
    )
    return result.returncode == 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
    else:
        command = "upgrade head"
    
    success = run_migration(command)
    sys.exit(0 if success else 1)

