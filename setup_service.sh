#!/bin/bash

# Script to setup systemd service for FastAPI
# Run with sudo

if [ "$EUID" -ne 0 ]
  then echo "Please run as root (sudo ./setup_service.sh)"
  exit
fi

echo "Setting up fastapi.service..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
fi

# Copy service file
cp fastapi.service /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Enable and start service
systemctl enable fastapi
systemctl restart fastapi

echo "Service fastapi started successfully!"
systemctl status fastapi --no-pager
