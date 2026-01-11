#!/bin/bash

# Script Setup Server Ubuntu untuk Matrix API
# Menjalankan Backend di Port 1101 via Nginx Reverse Proxy

# Exit on error
set -e

echo "=================================================="
echo "Memulai Setup Server Matrix API..."
echo "=================================================="

# 1. Update System
echo "[1/8] Mengupdate sistem..."
sudo apt-get update
sudo apt-get upgrade -y

# 2. Install Dependencies
echo "[2/8] Menginstall dependencies..."
sudo apt-get install -y python3-pip python3-venv postgresql postgresql-contrib nginx git libpq-dev python3-dev ufw acl

# 3. Konfigurasi Database
echo "[3/8] Mengkonfigurasi Database PostgreSQL..."
DB_NAME="matrix_massindo"
DB_USER="massindo"
DB_PASS="mas5indo"

# Start PostgreSQL service if not running
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create User if not exists
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
    echo "User $DB_USER dibuat."
else
    echo "User $DB_USER sudah ada."
    # Ensure password is correct
    sudo -u postgres psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASS';"
fi

# Create DB if not exists
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1; then
    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
    echo "Database $DB_NAME dibuat."
else
    echo "Database $DB_NAME sudah ada."
fi

# Grant Privileges
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
sudo -u postgres psql -d $DB_NAME -c "ALTER SCHEMA public OWNER TO $DB_USER;"

# 4. Setup Python Environment
echo "[4/8] Setup Python Virtual Environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment dibuat."
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Create .env File
echo "[5/8] Membuat file .env..."
cat > .env <<EOL
DATABASE_URL=postgresql://${DB_USER}:${DB_PASS}@localhost:5432/${DB_NAME}
ALLOWED_ORIGINS=http://103.164.99.2:1101,http://localhost:3000
EOL

# 6. Migrasi & Seeding
echo "[6/8] Menjalankan Migrasi & Seeding..."
# Note: seed.py will reset schema and run migrations automatically
python3 seed.py -y

# 7. Setup Systemd Service (Uvicorn)
echo "[7/8] Konfigurasi Systemd Service..."
CURRENT_USER=$(whoami)
CURRENT_GROUP=$(id -gn)
PROJECT_PATH=$(pwd)

SERVICE_FILE="/etc/systemd/system/fastapi_app.service"

sudo bash -c "cat > $SERVICE_FILE <<EOL
[Unit]
Description=FastAPI App (Matrix API)
After=network.target

[Service]
User=$CURRENT_USER
Group=$CURRENT_GROUP
WorkingDirectory=$PROJECT_PATH
Environment=\"PATH=$PROJECT_PATH/venv/bin\"
ExecStart=$PROJECT_PATH/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOL"

sudo systemctl daemon-reload
sudo systemctl enable fastapi_app
sudo systemctl restart fastapi_app

# 8. Setup Nginx
echo "[8/8] Konfigurasi Nginx..."
NGINX_CONF="/etc/nginx/sites-available/fastapi_app"

sudo bash -c "cat > $NGINX_CONF <<EOL
server {
    listen 1101;
    server_name 103.164.99.2;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOL"

# Enable site
if [ ! -L /etc/nginx/sites-enabled/fastapi_app ]; then
    sudo ln -s /etc/nginx/sites-available/fastapi_app /etc/nginx/sites-enabled/
fi

# Allow port 1101 in UFW
echo "Membuka port 1101 di Firewall..."
sudo ufw allow 1101/tcp
sudo ufw allow ssh  # Ensure SSH is not blocked
# sudo ufw enable  # Uncomment to enable firewall if not active

# Restart Nginx
sudo nginx -t
sudo systemctl restart nginx

echo "=================================================="
echo "Setup Selesai!"
echo "API dapat diakses di: http://103.164.99.2:1101/"
echo "Docs dapat diakses di: http://103.164.99.2:1101/docs"
echo "=================================================="
