#!/bin/bash

# Script untuk melakukan Full Reset dan Deploy di Ubuntu Server
# Melakukan: Git Pull -> Stop Service -> Reset DB -> Migrate -> Seed -> Restart Service

set -e  # Stop script jika ada error

echo "==========================================="
echo "   FULL RESET & DEPLOY SCRIPT"
echo "==========================================="

# 1. Git Pull
echo "[1/6] Pulling latest changes from Git..."
git pull origin main

# 2. Update Dependencies
echo "[2/6] Updating Python dependencies..."
# Asumsi virtualenv sudah aktif atau dipanggil lewat path absolute di systemd
# Kita aktifkan venv jika ada folder venv
if [ -d "venv" ]; then
    source venv/bin/activate
fi
pip install -r requirements.txt

# 3. Stop Service
echo "[3/6] Stopping FastAPI Service..."
if systemctl list-units --full -all | grep -Fq "fastapi.service"; then
    sudo systemctl stop fastapi
    echo "Service stopped."
else
    echo "Service 'fastapi' not found or not loaded. Skipping stop."
fi

# 4. Reset Database
echo "[4/6] Resetting Database (Drop & Create)..."
python reset_db.py

# 5. Migration & Seeding
echo "[5/6] Running Migrations and Seeding..."
alembic upgrade head
python seed.py

# 6. Restart Service
echo "[6/6] Restarting FastAPI Service..."
if systemctl list-units --full -all | grep -Fq "fastapi.service"; then
    sudo systemctl restart fastapi
    # Cek status
    if systemctl is-active --quiet fastapi; then
        echo "Service is RUNNING."
    else
        echo "WARNING: Service failed to start. Check logs with 'journalctl -u fastapi -e'"
    fi
else
    echo "Service 'fastapi' not configured. Skipping restart."
fi

echo "==========================================="
echo "   DEPLOYMENT FINISHED SUCCESSFULLY"
echo "==========================================="
