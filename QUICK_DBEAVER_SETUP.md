# ⚡ Quick Setup - DBeaver Connection

## 🚀 Quick Steps

### Untuk Database Lokal

1. **Buka DBeaver** → New Database Connection
2. **Pilih PostgreSQL**
3. **Isi:**
   - Host: `localhost`
   - Port: `5432`
   - Database: `nama_database`
   - Username: `postgres` (atau username Anda)
   - Password: `password_anda`
4. **Test Connection** → **Finish**

### Untuk Database Fly.io (Production)

#### Step 1: Get Connection String
```bash
# Via Fly.io CLI
fly postgres connect -a backend-fastapi-system-factory

# Atau dari Fly.io Dashboard → Secrets → DATABASE_URL
```

#### Step 2: Parse Connection String

Contoh connection string:
```
postgresql://user:pass@host.fly.dev:5432/dbname?sslmode=require
```

Extract:
- **Host**: `host.fly.dev`
- **Port**: `5432`
- **Database**: `dbname`
- **Username**: `user`
- **Password**: `pass`

#### Step 3: Setup di DBeaver

1. **New Database Connection** → **PostgreSQL**
2. **Main Tab:**
   - Host: `host.fly.dev`
   - Port: `5432`
   - Database: `dbname`
   - Username: `user`
   - Password: `pass`
3. **SSL Tab:**
   - ✅ Enable **Use SSL**
   - SSL Mode: `require`
4. **Test Connection** → **Finish**

## 📊 View Data

1. **Expand connection** → Databases → Schema → Tables
2. **Klik kanan tabel** → **View Data**
3. Atau buka **SQL Editor** dan jalankan query:
   ```sql
   SELECT * FROM production_logs;
   ```

## 🔍 Quick Queries

```sql
-- All production logs
SELECT * FROM production_logs ORDER BY created_at DESC;

-- With worker and item info
SELECT 
    pl.id,
    w.name AS worker,
    i.item_name,
    pl.qty_output,
    pl.qty_reject
FROM production_logs pl
JOIN workers w ON pl.worker_id = w.id
JOIN items i ON pl.item_id = i.id;
```

## ❌ Troubleshooting

**Connection Timeout?**
- Cek SSL enabled
- Cek firewall
- Cek network

**SSL Required?**
- Enable SSL di tab SSL
- Set mode ke `require`

**Wrong Password?**
- Double-check connection string
- Pastikan tidak ada typo

Lihat `DBeaver_Connection_Guide.md` untuk panduan lengkap.

