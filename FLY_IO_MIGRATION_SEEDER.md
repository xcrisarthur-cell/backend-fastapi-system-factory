# Migration dan Seeder di Fly.io

Panduan untuk menjalankan migration dan seeder database di backend yang sudah di-deploy di fly.io.

## 📋 Prerequisites

- Backend sudah di-deploy di fly.io
- Database PostgreSQL sudah ter-attach ke aplikasi
- Fly CLI sudah terinstall dan sudah login

## 🚀 Cara Menjalankan Migration

### Opsi 1: Menggunakan Fly SSH Console (Recommended)

1. **Masuk ke container via SSH:**
```powershell
cd backend-fastapi-system-factory
fly ssh console
```

2. **Setelah masuk ke container, jalankan migration:**
```bash
alembic upgrade head
```

3. **Verifikasi migration:**
```bash
alembic current
alembic history
```

4. **Keluar dari console:**
```bash
exit
```

### Opsi 2: Menggunakan Fly SSH Execute (One-liner)

Jalankan migration langsung tanpa masuk ke console:

```powershell
fly ssh console -C "alembic upgrade head"
```

Atau:

```powershell
fly ssh console -C "cd /app && alembic upgrade head"
```

### Opsi 3: Migration Otomatis (Sudah Dikonfigurasi)

Migration sudah otomatis berjalan saat aplikasi start (lihat `Dockerfile`). Tapi jika perlu menjalankan manual, gunakan opsi 1 atau 2.

## 🌱 Cara Menjalankan Seeder

### Opsi 1: Menggunakan Fly SSH Console (Recommended)

1. **Masuk ke container via SSH:**
```powershell
cd backend-fastapi-system-factory
fly ssh console
```

2. **Setelah masuk ke container, jalankan seeder:**
```bash
cd /app
python seed.py
```

3. **Ikuti prompt konfirmasi:**
   - Ketik `yes` atau `y` untuk melanjutkan
   - Seeder akan menghapus semua data yang ada dan mengisi data baru

4. **Keluar dari console:**
```bash
exit
```

### Opsi 2: Menggunakan Fly SSH Execute (Non-interactive)

Jika ingin menjalankan seeder tanpa konfirmasi interaktif, edit `seed.py` terlebih dahulu untuk skip konfirmasi, atau gunakan:

```powershell
fly ssh console -C "cd /app && echo 'yes' | python seed.py"
```

**⚠️ Peringatan:** Seeder akan menghapus semua data yang ada di database!

## 📝 Command Lengkap

### Migration

```powershell
# Cek status migration saat ini
fly ssh console -C "alembic current"

# Lihat history migration
fly ssh console -C "alembic history"

# Upgrade ke latest migration
fly ssh console -C "alembic upgrade head"

# Downgrade satu versi
fly ssh console -C "alembic downgrade -1"

# Downgrade semua (drop semua tabel)
fly ssh console -C "alembic downgrade base"
```

### Seeder

```powershell
# Jalankan seeder (dengan konfirmasi)
fly ssh console

# Di dalam console:
cd /app
python seed.py
# Ketik 'yes' untuk konfirmasi
exit
```

## 🔍 Verifikasi

Setelah migration dan seeder berhasil, verifikasi dengan:

1. **Cek logs aplikasi:**
```powershell
fly logs
```

2. **Test API endpoint:**
```powershell
# Test health check
curl https://backend-fastapi-system-factory.fly.dev/health

# Test workers endpoint
curl https://backend-fastapi-system-factory.fly.dev/workers
```

3. **Akses API docs:**
Buka di browser: https://backend-fastapi-system-factory.fly.dev/docs

## 🐛 Troubleshooting

### Error: "alembic: command not found"

Pastikan Anda sudah masuk ke container yang benar. Coba:

```powershell
fly ssh console -C "which alembic"
fly ssh console -C "python -m alembic upgrade head"
```

### Error: "DATABASE_URL not found"

Database URL sudah otomatis di-set oleh fly.io saat attach database. Jika error, cek:

```powershell
fly secrets list
```

Pastikan `DATABASE_URL` ada di secrets.

### Error: "Connection refused" atau "Connection timeout"

1. Pastikan database sudah ter-attach:
```powershell
fly postgres list
fly postgres attach --app backend-fastapi-system-factory mkp-operational
```

2. Cek status database:
```powershell
fly status
```

### Error: "Module not found"

Pastikan semua dependencies sudah terinstall. Cek `requirements.txt` dan pastikan sudah di-deploy dengan benar.

## 📚 Referensi

- [Fly.io SSH Documentation](https://fly.io/docs/flyctl/ssh/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [README_MIGRATION_SEEDER.md](./README_MIGRATION_SEEDER.md) - Dokumentasi lengkap migration dan seeder

---

**Catatan:** Migration sudah otomatis berjalan saat aplikasi start. Seeder perlu dijalankan manual jika ingin mengisi data awal.







