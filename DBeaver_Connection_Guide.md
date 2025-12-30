# 🗄️ DBeaver Connection Guide

Panduan lengkap untuk menghubungkan DBeaver ke database PostgreSQL MKP Operational System.

## 📋 Prerequisites

1. **DBeaver** sudah terinstall ([Download DBeaver](https://dbeaver.io/download/))
2. **PostgreSQL Driver** (otomatis terinstall dengan DBeaver)
3. **Database Connection String** (dari environment variable atau Fly.io)

## 🔧 Setup Connection

### Metode 1: Connect ke Database Lokal

Jika database PostgreSQL berjalan di localhost:

1. **Buka DBeaver**
2. **Klik "New Database Connection"** (ikon plug di toolbar) atau tekan `Ctrl+Shift+N`
3. **Pilih PostgreSQL** dari list database
4. **Isi Connection Settings:**
   - **Host**: `localhost` atau `127.0.0.1`
   - **Port**: `5432` (default PostgreSQL)
   - **Database**: nama database Anda (contoh: `mkp_operational`)
   - **Username**: username PostgreSQL (biasanya `postgres`)
   - **Password**: password PostgreSQL
5. **Klik "Test Connection"** untuk memastikan koneksi berhasil
6. **Klik "Finish"**

### Metode 2: Connect ke Database Fly.io (Production)

Database di Fly.io menggunakan PostgreSQL. Untuk connect, Anda perlu mendapatkan connection string terlebih dahulu.

#### Langkah 1: Get Database Connection String dari Fly.io

**Via Fly.io CLI:**
```bash
# List semua PostgreSQL databases
fly postgres list

# Get connection string (akan muncul di output)
fly postgres connect -a backend-fastapi-system-factory

# Atau get dari secrets
fly secrets list -a backend-fastapi-system-factory
```

**Via Fly.io Dashboard:**
1. Login ke [Fly.io Dashboard](https://fly.io/dashboard)
2. Pilih app `backend-fastapi-system-factory`
3. Buka **Secrets** tab
4. Cari `DATABASE_URL` - copy value-nya

**Format connection string biasanya:**
```
postgresql://username:password@hostname:port/database?sslmode=require
```

#### Langkah 2: Parse Connection String

**Cara Manual:**

Dari connection string, extract informasi berikut:
- **Host**: bagian setelah `@` dan sebelum `:`
- **Port**: setelah host (biasanya `5432`)
- **Database**: setelah port dan sebelum `?`
- **Username**: setelah `postgresql://` dan sebelum `:`
- **Password**: setelah username dan sebelum `@`
- **SSL Mode**: `require` (dari parameter `sslmode`)

**Contoh parsing:**
```
postgresql://mkp_operational:password123@mkp-operational-db.fly.dev:5432/mkp_operational?sslmode=require
```

Breakdown:
- Host: `mkp-operational-db.fly.dev`
- Port: `5432`
- Database: `mkp_operational`
- Username: `mkp_operational`
- Password: `password123`
- SSL Mode: `require`

**Cara Otomatis (Menggunakan Script):**

1. **Copy connection string** dari Fly.io
2. **Set environment variable:**
   ```bash
   # Windows PowerShell
   $env:DATABASE_URL="postgresql://user:pass@host:port/db?sslmode=require"
   
   # Windows CMD
   set DATABASE_URL=postgresql://user:pass@host:port/db?sslmode=require
   
   # Linux/Mac
   export DATABASE_URL="postgresql://user:pass@host:port/db?sslmode=require"
   ```
3. **Run script:**
   ```bash
   python parse_db_connection.py
   ```
4. Script akan menampilkan semua informasi yang diperlukan untuk DBeaver

#### Langkah 3: Setup Connection di DBeaver

1. **Buka DBeaver**
2. **Klik "New Database Connection"** (ikon plug) atau tekan `Ctrl+Shift+N`
3. **Pilih PostgreSQL**
4. **Tab "Main" - Isi Connection Settings:**
   - **Host**: `mkp-operational-db.fly.dev` (dari connection string)
   - **Port**: `5432`
   - **Database**: `mkp_operational` (dari connection string)
   - **Username**: `mkp_operational` (dari connection string)
   - **Password**: `password123` (dari connection string)
   - ✅ **Save password** (optional, untuk convenience)
5. **Tab "SSL" - Enable SSL:**
   - ✅ Enable **Use SSL**
   - **SSL Mode**: `require` atau `verify-full`
   - **SSL Factory**: Default (PostgreSQL)
6. **Klik "Test Connection"**
   - Jika berhasil, akan muncul "Connected"
   - Jika error, cek troubleshooting di bawah
7. **Klik "Finish"**

### Metode 3: Connect Menggunakan Connection String Langsung

DBeaver juga bisa menggunakan connection string langsung:

1. **Buka DBeaver**
2. **Klik "New Database Connection"**
3. **Pilih PostgreSQL**
4. **Klik tab "Main"**
5. **Di bagian bawah, klik "Edit Driver Settings"**
6. **Pilih tab "Connection Properties"**
7. **Add property baru:**
   - **Name**: `url`
   - **Value**: `jdbc:postgresql://host:port/database?sslmode=require`
8. **Atau gunakan "Connection URL" field** jika tersedia

## 📊 Melihat Data di Database

Setelah connection berhasil:

### 1. **Browse Tables**

1. Di **Database Navigator** (panel kiri), expand connection Anda
2. Expand **Databases** → **Database Name** → **Schemas** → **public** → **Tables**
3. Anda akan melihat semua tabel:
   - `divisions` - Divisi perusahaan
   - `departments` - Departemen per divisi
   - `positions` - Posisi pekerjaan
   - `sub_positions` - Sub posisi
   - `workers` - Data pekerja/operator
   - `shifts` - Shift kerja
   - `suppliers` - Supplier material
   - `items` - Item produk
   - `problem_comments` - Komentar masalah produksi
   - `production_logs` - Log produksi (tabel utama)
   - `production_log_problem_comments` - Relasi many-to-many

### 2. **View Table Data**

**Cara 1: Quick View**
1. **Klik kanan** pada tabel (contoh: `production_logs`)
2. Pilih **"View Data"** atau **"Open Data"**
3. Data akan ditampilkan di tab baru dengan pagination

**Cara 2: SQL Query**
1. **Klik kanan** pada tabel
2. Pilih **"Generate SQL"** → **"SELECT"**
3. Pilih kolom yang ingin ditampilkan
4. Klik **"Execute"**

### 3. **Run SQL Queries**

1. **Klik kanan** pada connection atau database
2. Pilih **"SQL Editor"** → **"New SQL Script"** atau tekan `Ctrl+]`
3. Tulis query SQL, contoh:
   ```sql
   -- Get all production logs
   SELECT * FROM production_logs ORDER BY created_at DESC LIMIT 100;
   
   -- Get production logs with worker and item info
   SELECT 
       pl.id,
       pl.created_at,
       w.name AS worker_name,
       p.code AS position_code,
       s.name AS shift_name,
       i.item_name,
       i.item_number,
       pl.qty_output,
       pl.qty_reject,
       pl.approved_coordinator,
       pl.approved_spv
   FROM production_logs pl
   LEFT JOIN workers w ON pl.worker_id = w.id
   LEFT JOIN positions p ON pl.position_id = p.id
   LEFT JOIN shifts s ON pl.shift_id = s.id
   LEFT JOIN items i ON pl.item_id = i.id
   ORDER BY pl.created_at DESC
   LIMIT 50;
   ```
4. **Klik "Execute SQL Script"** (ikon play) atau tekan `Ctrl+Enter`
5. Hasil akan muncul di tab **Data** di bawah

### 4. **Query Builder (Visual)**

1. **Klik kanan** pada tabel
2. Pilih **"Generate SQL"** → **"SELECT"**
3. Pilih kolom yang ingin ditampilkan
4. Set filter, sorting, grouping, dll
5. Klik **"Generate"** untuk melihat SQL
6. Klik **"Execute"** untuk menjalankan

### 5. **Export Data**

1. **Select data** dari query result atau table view
2. **Klik kanan** pada data
3. Pilih **"Export Data"**
4. Pilih format:
   - **CSV** - untuk Excel
   - **Excel** - langsung ke Excel
   - **JSON** - untuk API testing
   - **SQL** - untuk backup
5. Pilih destination dan klik **"Start"**

## 🔍 Contoh Queries Berguna

### View All Production Logs
```sql
SELECT * FROM production_logs 
ORDER BY created_at DESC 
LIMIT 100;
```

### Production Logs dengan Detail Lengkap
```sql
SELECT 
    pl.id,
    pl.created_at,
    w.name AS worker_name,
    p.code AS position_code,
    sp.code AS sub_position_code,
    s.name AS shift_name,
    i.item_name,
    i.item_number,
    pl.qty_output,
    pl.qty_reject,
    pl.problem_duration_minutes,
    pl.approved_coordinator,
    pl.approved_spv,
    pl.approved_coordinator_at,
    pl.approved_spv_at
FROM production_logs pl
LEFT JOIN workers w ON pl.worker_id = w.id
LEFT JOIN positions p ON pl.position_id = p.id
LEFT JOIN sub_positions sp ON pl.sub_position_id = sp.id
LEFT JOIN shifts s ON pl.shift_id = s.id
LEFT JOIN items i ON pl.item_id = i.id
ORDER BY pl.created_at DESC;
```

### Statistics - Total Production
```sql
SELECT 
    COUNT(*) AS total_logs,
    SUM(qty_output) AS total_output,
    SUM(qty_reject) AS total_reject,
    ROUND((SUM(qty_reject) / NULLIF(SUM(qty_output), 0)) * 100, 2) AS rejection_rate_percent
FROM production_logs;
```

### Production per Worker
```sql
SELECT 
    w.id,
    w.name AS worker_name,
    COUNT(pl.id) AS log_count,
    SUM(pl.qty_output) AS total_output,
    SUM(pl.qty_reject) AS total_reject,
    ROUND(AVG(pl.qty_output), 2) AS avg_output
FROM production_logs pl
JOIN workers w ON pl.worker_id = w.id
GROUP BY w.id, w.name
ORDER BY total_output DESC;
```

### Production per Item
```sql
SELECT 
    i.id,
    i.item_number,
    i.item_name,
    COUNT(pl.id) AS log_count,
    SUM(pl.qty_output) AS total_output,
    SUM(pl.qty_reject) AS total_reject
FROM production_logs pl
JOIN items i ON pl.item_id = i.id
GROUP BY i.id, i.item_number, i.item_name
ORDER BY total_output DESC;
```

### Production per Shift
```sql
SELECT 
    s.name AS shift_name,
    COUNT(pl.id) AS log_count,
    SUM(pl.qty_output) AS total_output,
    SUM(pl.qty_reject) AS total_reject
FROM production_logs pl
JOIN shifts s ON pl.shift_id = s.id
GROUP BY s.id, s.name
ORDER BY s.name;
```

### Approval Status
```sql
SELECT 
    COUNT(*) AS total,
    COUNT(CASE WHEN approved_coordinator = true THEN 1 END) AS approved_coordinator,
    COUNT(CASE WHEN approved_coordinator IS NULL OR approved_coordinator = false THEN 1 END) AS pending_coordinator,
    COUNT(CASE WHEN approved_spv = true THEN 1 END) AS approved_spv,
    COUNT(CASE WHEN approved_spv IS NULL OR approved_spv = false THEN 1 END) AS pending_spv
FROM production_logs;
```

### Production Logs dengan Problem Comments
```sql
SELECT 
    pl.id,
    pl.created_at,
    w.name AS worker_name,
    i.item_name,
    pl.qty_output,
    pl.qty_reject,
    STRING_AGG(pc.description, ', ') AS problem_comments
FROM production_logs pl
LEFT JOIN workers w ON pl.worker_id = w.id
LEFT JOIN items i ON pl.item_id = i.id
LEFT JOIN production_log_problem_comments plpc ON pl.id = plpc.production_log_id
LEFT JOIN problem_comments pc ON plpc.problem_comment_id = pc.id
GROUP BY pl.id, pl.created_at, w.name, i.item_name, pl.qty_output, pl.qty_reject
ORDER BY pl.created_at DESC;
```

## 🛠️ Troubleshooting

### Connection Timeout

**Error**: Connection timeout atau tidak bisa connect

**Solusi**:
1. **Cek database sudah running** (untuk local database)
2. **Cek firewall settings** - pastikan port 5432 tidak di-block
3. **Untuk Fly.io**, pastikan menggunakan SSL
4. **Cek network connection** - pastikan internet stabil
5. **Cek host dan port** - pastikan benar

### SSL Required Error

**Error**: `SSL connection is required` atau `no pg_hba.conf entry`

**Solusi**:
1. Di DBeaver connection settings, buka tab **SSL**
2. ✅ Enable **Use SSL**
3. Set **SSL Mode** ke `require` atau `verify-full`
4. **Test connection** lagi
5. Untuk Fly.io, SSL **wajib** diaktifkan

### Authentication Failed

**Error**: `password authentication failed for user`

**Solusi**:
1. **Double-check username dan password** - pastikan tidak ada typo
2. **Untuk Fly.io**, pastikan connection string sudah benar
3. **Cek apakah user memiliki permission** untuk database
4. **Coba reset password** jika perlu

### Database Not Found

**Error**: `database "xxx" does not exist`

**Solusi**:
1. **Pastikan nama database benar** - cek connection string
2. **Cek database name** di connection string, pastikan setelah port dan sebelum `?`
3. **Untuk Fly.io**, database name biasanya ada di connection string
4. **List databases** untuk melihat database yang tersedia:
   ```sql
   SELECT datname FROM pg_database;
   ```

### Connection Refused

**Error**: `Connection refused` atau `Could not connect to server`

**Solusi**:
1. **Cek PostgreSQL service** sudah running (untuk local)
2. **Cek port** - pastikan 5432 (atau port yang benar)
3. **Cek host** - pastikan hostname benar
4. **Untuk Fly.io**, pastikan menggunakan hostname yang benar dari connection string

### Driver Not Found

**Error**: `Driver not found` atau `PostgreSQL driver missing`

**Solusi**:
1. **Download PostgreSQL driver** di DBeaver:
   - Edit connection → Driver properties → Download
2. **Atau install manual**:
   - Help → DBeaver → Driver Manager
   - Find PostgreSQL → Download

## 📝 Tips & Best Practices

### 1. **Organize Connections**

- **Buat connection groups** untuk organize:
  - Production
  - Development
  - Staging
- **Rename connections** dengan nama yang jelas
- **Add descriptions** untuk setiap connection

### 2. **Save Frequently Used Queries**

1. **Buat SQL Script** dengan query yang sering digunakan
2. **Save di folder** yang terorganisir
3. **Add to favorites** untuk quick access

### 3. **Data Export & Import**

- **Export data** ke CSV/Excel untuk analisis
- **Import data** dari CSV untuk bulk insert
- **Backup database** secara berkala

### 4. **ER Diagram**

DBeaver bisa generate ER diagram:
1. **Klik kanan** pada database
2. Pilih **"View Diagram"**
3. Pilih tabel yang ingin ditampilkan
4. DBeaver akan generate visual ER diagram

### 5. **Table Statistics**

Lihat statistics tabel:
1. **Klik kanan** pada tabel
2. Pilih **"View Statistics"**
3. Lihat row count, size, indexes, dll

### 6. **Search Data**

1. **Klik kanan** pada database
2. Pilih **"Find in Database"**
3. Masukkan keyword
4. Pilih tabel yang ingin dicari
5. DBeaver akan search di semua kolom

## 🔐 Security Notes

⚠️ **Penting untuk Production Database:**

1. **Jangan commit connection string** ke Git
2. **Gunakan environment variables** untuk sensitive data
3. **Limit access** ke production database - hanya user yang perlu
4. **Use read-only user** jika hanya perlu melihat data
5. **Enable SSL** untuk semua production connections
6. **Don't save password** di DBeaver jika komputer shared
7. **Use VPN** jika memungkinkan untuk extra security

## 📚 Referensi

- [DBeaver Documentation](https://dbeaver.com/docs/)
- [PostgreSQL Connection Guide](https://www.postgresql.org/docs/current/libpq-connect.html)
- [Fly.io PostgreSQL Guide](https://fly.io/docs/postgres/)
- [PostgreSQL SQL Reference](https://www.postgresql.org/docs/current/sql.html)

## 🆘 Quick Help

Jika masih ada masalah:
1. Cek `QUICK_DBEAVER_SETUP.md` untuk quick reference
2. Cek DBeaver logs: Help → View Log
3. Test connection dengan `psql` command line tool
4. Cek database logs untuk error details
