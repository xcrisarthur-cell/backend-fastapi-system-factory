#!/bin/bash

# Deploy Script for Backend FastAPI System Factory
# Usage: ./deploy.sh [setup|update]

set -e  # Exit immediately if a command exits with a non-zero status

# Function to display usage
usage() {
    echo "Usage: $0 [setup|update]"
    echo "  setup  : Run initial setup (install deps, RESET database, seed data)"
    echo "           WARNING: This will WIPE existing data!"
    echo "  update : Update application (git pull, install deps, migrate only)"
    echo "           This preserves data and only updates the database structure."
    exit 1
}

# Check if argument is provided
if [ $# -eq 0 ]; then
    usage
fi

MODE=$1

# Check for .env file
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create a .env file with your database credentials."
    exit 1
fi

echo "==========================================="
echo "   Backend Deployment Script - $MODE"
echo "==========================================="

if [ "$MODE" == "setup" ]; then
    echo "[1/3] Installing dependencies..."
    pip install -r requirements.txt
    
    echo "[2/3] Initializing Database & Seeding..."
    echo "WARNING: This will drop all tables and recreate them."
    # seed.py handles dropping tables, running migrations, and seeding
    python seed.py --yes
    
    echo "==========================================="
    echo "   Setup Complete!"
    echo "==========================================="

elif [ "$MODE" == "update" ]; then
    echo "[1/3] Pulling latest changes from GitHub..."
    git pull
    
    echo "[2/3] Installing/Updating dependencies..."
    pip install -r requirements.txt
    
    echo "[3/3] Running Database Migrations..."
    # This updates existing tables without deleting data
    alembic upgrade head
    
    echo "==========================================="
    echo "   Update Complete!"
    echo "==========================================="
    
else
    usage
fi
