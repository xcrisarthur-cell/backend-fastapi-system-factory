# Quick Start Guide - Migration & Seeder

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
Pastikan `.env` file sudah ada dengan `DATABASE_URL`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```

### 3. Run Migration
```bash
# Create all tables
alembic upgrade head
```

Atau menggunakan helper script:
```bash
python run_migration.py upgrade head
```

### 4. Seed Database
```bash
python seed.py
```

**Note**: Seeder akan menghapus semua data yang ada sebelum mengisi data baru.

## 📊 Data yang Akan Dibuat

- ✅ 5 Divisions
- ✅ 15 Departments (3 per division)
- ✅ 10 Positions
- ✅ 20 Sub Positions (2 per position)
- ✅ 50 Workers
- ✅ 3 Shifts
- ✅ 10 Suppliers
- ✅ 30 Items
- ✅ 15 Problem Comments
- ✅ 200 Production Logs
- ✅ ~80 Production Log Problem Comment Links

## 🔄 Reset Database

```bash
# Drop all tables
alembic downgrade base

# Create tables again
alembic upgrade head

# Seed new data
python seed.py
```

## 📚 Dokumentasi Lengkap

Lihat `README_MIGRATION_SEEDER.md` untuk dokumentasi lengkap.

