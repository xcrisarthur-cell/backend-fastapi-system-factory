# Migration dan Seeder Guide

## 📋 Deskripsi

Dokumentasi untuk menjalankan migration database dan seeder data untuk Matrix System.

## 🚀 Setup Awal

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies yang diperlukan:
- `alembic` - untuk database migration
- `faker` - untuk generate data random

### 2. Konfigurasi Database

Pastikan file `.env` sudah dikonfigurasi dengan `DATABASE_URL`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```

## 📦 Migration

### Menjalankan Migration

Migration akan membuat semua tabel sesuai dengan schema database.

```bash
# Upgrade database (create tables)
alembic upgrade head

# Downgrade database (drop tables)
alembic downgrade base
```

### Membuat Migration Baru

Jika ada perubahan model, buat migration baru:

```bash
# Auto-generate migration dari perubahan model
alembic revision --autogenerate -m "description"

# Manual migration
alembic revision -m "description"
```

### Melihat Status Migration

```bash
# Lihat current revision
alembic current

# Lihat history
alembic history
```

## 🌱 Seeder

### Menjalankan Seeder

Seeder akan mengisi database dengan data random menggunakan Faker.

```bash
python seed.py
```

**Peringatan**: Seeder akan **menghapus semua data yang ada** di database sebelum mengisi data baru.

### Data yang Dihasilkan

Seeder akan membuat data berikut:

| Tabel | Jumlah Default | Deskripsi |
|-------|--------------|-----------|
| Divisions | 5 | Divisi operasional |
| Departments | 15 (3 per division) | Departemen per divisi |
| Positions | 10 | Posisi pekerjaan |
| Sub Positions | 20 (2 per position) | Sub posisi |
| Workers | 50 | Pekerja dengan posisi dan departemen |
| Shifts | 3 | Shift kerja (A, B, C) |
| Suppliers | 10 | Supplier material |
| Items | 30 | Item produk |
| Problem Comments | 15 | Komentar masalah produksi |
| Production Logs | 200 | Log produksi dengan approval status |
| Production Log Problem Comments | ~80 | Relasi many-to-many |

### Mengubah Jumlah Data

Edit file `seed.py` dan ubah parameter `count` di setiap fungsi:

```python
# Contoh: ubah jumlah workers menjadi 100
workers = seed_workers(db, positions, departments, count=100)
```

## 📝 Struktur File

```
backend/
├── alembic/
│   ├── versions/
│   │   └── 001_initial_migration.py  # Initial migration
│   ├── env.py                         # Alembic configuration
│   └── script.py.mako                 # Migration template
├── alembic.ini                        # Alembic config file
├── seed.py                            # Seeder script
└── README_MIGRATION_SEEDER.md         # Dokumentasi ini
```

## 🔄 Workflow Lengkap

### Setup Database Baru

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migration
alembic upgrade head

# 3. Run seeder
python seed.py
```

### Reset Database

```bash
# 1. Downgrade (drop semua tabel)
alembic downgrade base

# 2. Upgrade (create tabel lagi)
alembic upgrade head

# 3. Seed data baru
python seed.py
```

## 🎲 Data Random

Seeder menggunakan **Faker** dengan locale Indonesia (`id_ID`) untuk generate:
- Nama pekerja (Indonesian names)
- Nama perusahaan/supplier
- Deskripsi dan spesifikasi
- Tanggal dan waktu

Data di-generate dengan seed yang sama untuk reproducibility.

## ⚠️ Catatan Penting

1. **Backup Database**: Selalu backup database sebelum menjalankan seeder
2. **Foreign Keys**: Seeder menghormati foreign key constraints
3. **Unique Constraints**: Data di-generate dengan kode unik untuk menghindari conflict
4. **Approval Status**: Production logs memiliki random approval status (coordinator & SPV)
5. **Many-to-Many**: Production logs linked dengan problem comments secara random

## 🐛 Troubleshooting

### Error: "Table already exists"
```bash
# Drop semua tabel dulu
alembic downgrade base
# Lalu upgrade lagi
alembic upgrade head
```

### Error: "Foreign key constraint"
- Pastikan seeder dijalankan dalam urutan yang benar
- Check apakah parent records sudah ada

### Error: "Connection refused"
- Pastikan database server berjalan
- Check `DATABASE_URL` di file `.env`

### Error: "Module not found"
```bash
# Install dependencies
pip install -r requirements.txt
```

## 📚 Referensi

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Faker Documentation](https://faker.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

**Happy Seeding! 🌱**

