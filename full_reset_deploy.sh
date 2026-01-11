#!/bin/bash

# Script 2: FULL RESET & DEPLOY
# Digunakan untuk reset total: Git Pull -> Reset DB (Drop All) -> Migrate -> Seed -> Restart

set -e

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
SERVICE_NAME="fastapi"

echo "==========================================="
echo "   FULL RESET & DEPLOY SCRIPT"
echo "==========================================="
echo "Project Directory: $PROJECT_DIR"

# 1. Git Pull
echo -e "\n[1/6] Pulling latest changes..."
cd "$PROJECT_DIR"
git pull origin main

# 2. Python Environment
echo -e "\n[2/6] Setting up Python environment..."
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

echo "Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# 3. Stop Service (to unlock DB)
echo -e "\n[3/6] Stopping Service..."
if command -v systemctl &> /dev/null; then
    if systemctl list-units --full -all | grep -Fq "$SERVICE_NAME.service"; then
        sudo systemctl stop $SERVICE_NAME
        echo "Service stopped."
    fi
fi

# 4. Reset Database
echo -e "\n[4/6] Resetting Database..."
# Menjalankan reset_db.py yang akan menghapus semua tabel
python reset_db.py

# 5. Migration & Seeding
echo -e "\n[5/6] Running Migrations & Seeder..."
# Membuat tabel baru
alembic upgrade head

# Mengisi data awal
# Flag --yes untuk skip konfirmasi, tapi JANGAN gunakan --seed-only karena kita butuh reset logic di seed.py juga jika ada yang terlewat
# Atau jika seed.py menghandle reset schema juga, kita bisa langsung pakai seed.py tanpa alembic upgrade head di awal
# Tapi amannya: alembic dulu, baru seed dengan flag --seed-only
python seed.py --yes --seed-only

# 6. Restart Service
echo -e "\n[6/6] Restarting Service..."
if command -v systemctl &> /dev/null; then
    if systemctl list-units --full -all | grep -Fq "$SERVICE_NAME.service"; then
        sudo systemctl restart $SERVICE_NAME
        echo "Service '$SERVICE_NAME' restarted."
    else
        echo "Service '$SERVICE_NAME' not found in systemd. Skipping restart."
        echo "If running locally, you can start the server with: ./start.sh"
    fi
else
    echo "systemctl not found. Skipping service restart (Local mode)."
fi

echo -e "\n==========================================="
echo "   FULL RESET FINISHED SUCCESSFULLY"
echo "==========================================="
