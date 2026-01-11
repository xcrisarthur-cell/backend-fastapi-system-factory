# Quick Start Guide - Environment Automation

## 🚀 One-Command Setup

Untuk setup environment lengkap (Database, Migration, Seeding) dan menjalankan server dalam satu perintah:

```bash
./start.sh
```

Script ini akan otomatis:
1.  **Cek & Buat Database**: Jika database belum ada, akan dibuat otomatis.
2.  **Jalankan Migrasi**: Memastikan struktur tabel sesuai dengan schema terbaru (`alembic upgrade head`).
3.  **Jalankan Seeder**: Mengisi/Update data master (Division, Dept, Workers, dll) jika belum ada.
4.  **Jalankan Server**: Menjalankan server FastAPI (`uvicorn`) di port 8000.

---

## 🛠 Manual Setup (Jika diperlukan)

Jika Anda ingin menjalankan langkah-langkah secara terpisah:

### 1. Setup Environment & Database
Menggunakan script manager:
```bash
python manage.py
```
Perintah ini akan melakukan pengecekan database, migrasi, dan seeding tanpa menjalankan server.

### 2. Jalankan Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📝 Configuration

Pastikan file `.env` Anda memiliki konfigurasi database yang benar:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```

## 🧹 Cleaning Up

Jika Anda ingin mereset total database (HATI-HATI: Data akan hilang):
1.  Drop database secara manual di PostgreSQL.
2.  Jalankan `./start.sh` atau `python manage.py` untuk membuat ulang dari nol.
