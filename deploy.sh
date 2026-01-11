#!/bin/bash

# Script 1: UPDATE & DEPLOY
# Digunakan untuk update rutin: Git Pull -> Install Deps -> Cek DB/Migrate -> Restart

set -e

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
SERVICE_NAME="fastapi"

echo "==========================================="
echo "   UPDATE & DEPLOY SCRIPT"
echo "==========================================="
echo "Project Directory: $PROJECT_DIR"

# 1. Git Pull
echo -e "\n[1/5] Pulling latest changes..."
cd "$PROJECT_DIR"
git pull origin main

# 2. Python Environment
echo -e "\n[2/5] Setting up Python environment..."
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

echo "Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# 3. Database Check & Migration
echo -e "\n[3/5] Checking Database & Migrations..."

# Check DB Connection
python -c "
import os, sys, psycopg2
from dotenv import load_dotenv
load_dotenv()
try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    conn.close()
    print('Database connection OK.')
except Exception as e:
    print(f'Error connecting to database: {e}')
    sys.exit(1)
"

# Run Migrations
echo "Running Alembic Migrations..."
alembic upgrade head

# 4. Restart Service
echo -e "\n[4/5] Restarting Service..."
if command -v systemctl &> /dev/null; then
    if systemctl list-units --full -all | grep -Fq "$SERVICE_NAME.service"; then
        sudo systemctl restart $SERVICE_NAME
        echo "Service '$SERVICE_NAME' restarted."
    else
        echo "Service '$SERVICE_NAME' not found in systemd. Skipping restart."
        echo "If running locally, please restart your uvicorn process manually."
    fi
else
    echo "systemctl not found. Skipping service restart (Local mode)."
fi

echo -e "\n==========================================="
echo "   UPDATE FINISHED SUCCESSFULLY"
echo "==========================================="
