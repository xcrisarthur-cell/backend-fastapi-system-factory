#!/bin/bash
set -e

echo "==========================================="
echo "   🚀 SETUP MANUAL BACKEND (LOCAL) "
echo "==========================================="

# 1. Install Dependencies
echo "[1/5] 📦 Installing Python dependencies..."
pip install -r requirements.txt

# 2. Initialize Database (Create User & DB)
echo "[2/5] 🐘 Setup PostgreSQL Database..."
python init_db_local.py

# 3. Run Migrations
echo "[3/5] 🔄 Running Migrations..."
alembic upgrade head

# 4. Seed Data
echo "[4/5] 🌱 Seeding Data..."
# seed.py --yes to skip confirmation
python seed.py --yes

# 5. Start Server
echo "==========================================="
echo "   ✅ SETUP FINISHED! STARTING SERVER..."
echo "==========================================="
echo "🌐 Server running at: http://127.0.0.1:8000"
echo "📚 Documentation at : http://127.0.0.1:8000/docs"
echo "Tekan Ctrl+C untuk berhenti."
echo ""

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
