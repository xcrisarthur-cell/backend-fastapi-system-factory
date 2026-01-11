#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting backend setup..."

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed or not in PATH."
    exit 1
fi

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing/Updating dependencies..."
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found."
fi

# Run the management script to setup DB, migrate, and seed
echo "Running manage.py..."
python manage.py

echo "Starting Uvicorn server..."
# Start the FastAPI application
exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
