#!/bin/bash

# Script untuk update aplikasi, reset database, dan seed ulang
# Pastikan dijalankan dari root folder project

echo "========================================================"
echo "Matrix Update & Reset Database Script"
echo "========================================================"

# 1. Update kode dari Git
echo -e "\n1. Menarik update terbaru dari Git..."
git fetch --all
git reset --hard origin/main
git pull origin main

# 2. Rebuild container (jika ada perubahan dependensi/Dockerfile)
echo -e "\n2. Rebuild dan restart container..."
sudo docker compose down
sudo docker compose up -d --build

# 3. Tunggu sebentar agar database siap
echo -e "\n3. Menunggu database siap (10 detik)..."
sleep 10

# 4. Reset Database & Seeding
# Flag --yes akan melewati konfirmasi manual di seed.py
echo -e "\n4. Reset Database & Seeding..."
sudo docker compose exec app python seed.py --yes

echo -e "\n========================================================"
echo "Update dan Reset Selesai!"
echo "API Backend berjalan di port 1101 (via Nginx) atau 8000 (Local)"
echo "========================================================"
