# Database Schema Documentation

## 📋 Overview

Database schema untuk **MKP Operational System Factory** menggunakan PostgreSQL.

## 🗂️ Database Structure

### Tables

1. **divisions** - Divisi dalam organisasi
2. **departments** - Departemen dalam divisi
3. **positions** - Posisi pekerjaan
4. **sub_positions** - Sub posisi atau mesin
5. **workers** - Pekerja/operator
6. **shifts** - Shift kerja
7. **suppliers** - Supplier material
8. **items** - Item produk
9. **problem_comments** - Jenis kendala produksi
10. **production_logs** - Log produksi harian
11. **production_log_problem_comments** - Relasi many-to-many

## 📊 Entity Relationship Diagram (ERD)

```
divisions (1) ──< (N) departments
departments (1) ──< (N) workers
positions (1) ──< (N) sub_positions
positions (1) ──< (N) workers
positions (1) ──< (N) production_logs
workers (1) ──< (N) production_logs
workers (1) ──< (N) production_logs (approved_coordinator_by)
workers (1) ──< (N) production_logs (approved_spv_by)
shifts (1) ──< (N) production_logs
suppliers (1) ──< (N) production_logs
items (1) ──< (N) production_logs
sub_positions (1) ──< (N) production_logs
problem_comments (N) ──< (N) production_logs (via production_log_problem_comments)
```

## 📝 Table Details

### 1. divisions

Divisi dalam organisasi.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-increment ID |
| code | VARCHAR(20) | UNIQUE, NOT NULL | Kode divisi (e.g., DIV001) |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Nama divisi (e.g., Kawat, IT) |

**Relationships:**
- Has many: `departments`

---

### 2. departments

Departemen dalam divisi.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-increment ID |
| division_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to divisions.id |
| code | VARCHAR(20) | NOT NULL | Kode departemen (e.g., DEPT01) |
| name | VARCHAR(100) | NOT NULL | Nama departemen (e.g., Operator, Koordinator) |

**Constraints:**
- Unique: `(division_id, code)` - Kode departemen unik per divisi

**Relationships:**
- Belongs to: `division`
- Has many: `workers`

---

### 3. positions

Posisi pekerjaan.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-increment ID |
| code | VARCHAR(20) | UNIQUE, NOT NULL | Kode posisi (e.g., PER, RAM, TEMBAK) |
| unit | VARCHAR(10) | NOT NULL, CHECK | Unit pengukuran: 'pcs' atau 'lmbr' |

**Constraints:**
- Check: `unit IN ('pcs', 'lmbr')`

**Relationships:**
- Has many: `sub_positions`
- Has many: `workers`
- Has many: `production_logs`

---

### 4. sub_positions

Sub posisi atau mesin dalam posisi.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-increment ID |
| position_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to positions.id |
| code | VARCHAR(30) | NOT NULL | Kode sub posisi (e.g., FC60, SX80, MEJA-1) |

**Constraints:**
- Unique: `(position_id, code)` - Kode sub posisi unik per posisi

**Relationships:**
- Belongs to: `position`
- Has many: `production_logs`

---

### 5. workers

Pekerja/operator dalam sistem.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-increment ID |
| name | VARCHAR(100) | NOT NULL | Nama pekerja |
| password | VARCHAR(255) | NULLABLE | Password ter-hash untuk autentikasi |
| position_id | INTEGER | FOREIGN KEY, NULLABLE | Reference to positions.id |
| department_id | INTEGER | FOREIGN KEY, NULLABLE | Reference to departments.id |

**Relationships:**
- Belongs to: `position` (optional)
- Belongs to: `department` (optional)
- Has many: `production_logs` (as worker)
- Has many: `production_logs` (as approved_coordinator_by)
- Has many: `production_logs` (as approved_spv_by)

---

### 6. shifts

Shift kerja.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-increment ID |
| name | VARCHAR(20) | UNIQUE, NOT NULL | Nama shift (e.g., Shift 1, Shift 2, Shift 3) |

**Relationships:**
- Has many: `production_logs`

---

### 7. suppliers

Supplier material.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-increment ID |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Nama supplier (e.g., Intiroda, Mega, Kingdom) |

**Relationships:**
- Has many: `production_logs`

---

### 8. items

Item produk yang diproduksi.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-increment ID |
| item_number | VARCHAR(50) | UNIQUE, NOT NULL | Nomor item (e.g., W1090001581224) |
| item_name | VARCHAR(100) | NULLABLE | Nama item |
| spec | TEXT | NULLABLE | Spesifikasi item |

**Relationships:**
- Has many: `production_logs`

---

### 9. problem_comments

Jenis kendala produksi.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-increment ID |
| description | VARCHAR(255) | UNIQUE, NOT NULL | Deskripsi kendala (e.g., Mesin rusak, Kekurangan material) |

**Relationships:**
- Has many: `production_log_problem_comments` (many-to-many with production_logs)

---

### 10. production_logs

Log produksi harian.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BIGINT | PRIMARY KEY | Auto-increment ID |
| worker_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to workers.id |
| position_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to positions.id |
| sub_position_id | INTEGER | FOREIGN KEY, NULLABLE | Reference to sub_positions.id |
| shift_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to shifts.id |
| supplier_id | INTEGER | FOREIGN KEY, NULLABLE | Reference to suppliers.id |
| item_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to items.id |
| qty_output | NUMERIC(10,2) | NOT NULL, CHECK >= 0 | Jumlah output produksi |
| qty_reject | NUMERIC(10,2) | NOT NULL, CHECK >= 0 | Jumlah reject produksi |
| problem_duration_minutes | INTEGER | NULLABLE, CHECK >= 0 | Durasi kendala dalam menit |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Waktu pembuatan log |
| approved_coordinator | BOOLEAN | NULLABLE | Status approval oleh koordinator |
| approved_spv | BOOLEAN | NULLABLE | Status approval oleh supervisor |
| approved_coordinator_at | TIMESTAMP | NULLABLE | Waktu approval oleh koordinator |
| approved_spv_at | TIMESTAMP | NULLABLE | Waktu approval oleh supervisor |
| approved_coordinator_by | INTEGER | FOREIGN KEY, NULLABLE | Reference to workers.id (koordinator) |
| approved_spv_by | INTEGER | FOREIGN KEY, NULLABLE | Reference to workers.id (supervisor) |

**Constraints:**
- Check: `qty_output >= 0`
- Check: `qty_reject >= 0`
- Check: `problem_duration_minutes >= 0`
- Check: `(approved_spv IS NULL) OR (approved_coordinator = true)` - SPV hanya bisa approve jika sudah di-approve coordinator

**Relationships:**
- Belongs to: `worker`
- Belongs to: `position`
- Belongs to: `sub_position` (optional)
- Belongs to: `shift`
- Belongs to: `supplier` (optional)
- Belongs to: `item`
- Belongs to: `approved_coordinator_by_worker` (optional)
- Belongs to: `approved_spv_by_worker` (optional)
- Has many: `production_log_problem_comments` (many-to-many with problem_comments)

---

### 11. production_log_problem_comments

Relasi many-to-many antara production_logs dan problem_comments.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Auto-increment ID |
| production_log_id | BIGINT | FOREIGN KEY, NOT NULL, CASCADE | Reference to production_logs.id |
| problem_comment_id | INTEGER | FOREIGN KEY, NOT NULL, RESTRICT | Reference to problem_comments.id |

**Constraints:**
- Unique: `(production_log_id, problem_comment_id)` - Satu kendala hanya bisa di-assign sekali per log

**Relationships:**
- Belongs to: `production_log`
- Belongs to: `problem_comment`

---

## 🔑 Foreign Key Relationships

### Cascade Rules

- **CASCADE**: `production_log_problem_comments.production_log_id` - Jika production_log dihapus, relasi juga dihapus
- **RESTRICT**: Semua foreign key lainnya - Mencegah penghapusan jika masih ada referensi

### Foreign Key Summary

| Table | Column | References | On Delete |
|-------|--------|------------|-----------|
| departments | division_id | divisions.id | RESTRICT |
| sub_positions | position_id | positions.id | RESTRICT |
| workers | position_id | positions.id | RESTRICT |
| workers | department_id | departments.id | RESTRICT |
| production_logs | worker_id | workers.id | (default) |
| production_logs | position_id | positions.id | (default) |
| production_logs | sub_position_id | sub_positions.id | (default) |
| production_logs | shift_id | shifts.id | (default) |
| production_logs | supplier_id | suppliers.id | (default) |
| production_logs | item_id | items.id | (default) |
| production_logs | approved_coordinator_by | workers.id | (default) |
| production_logs | approved_spv_by | workers.id | (default) |
| production_log_problem_comments | production_log_id | production_logs.id | CASCADE |
| production_log_problem_comments | problem_comment_id | problem_comments.id | RESTRICT |

## 📈 Sequences

Semua tabel menggunakan PostgreSQL sequences untuk auto-increment:

- `divisions_id_seq`
- `departments_id_seq`
- `positions_id_seq`
- `sub_positions_id_seq`
- `workers_id_seq`
- `shifts_id_seq`
- `suppliers_id_seq`
- `items_id_seq`
- `problem_comments_id_seq`
- `production_logs_id_seq` (BIGINT)
- `production_log_problem_comments_id_seq`

## ✅ Constraints Summary

### Unique Constraints

- `divisions.code`
- `divisions.name`
- `departments(division_id, code)` - Composite unique
- `positions.code`
- `sub_positions(position_id, code)` - Composite unique
- `shifts.name`
- `suppliers.name`
- `items.item_number`
- `problem_comments.description`
- `production_log_problem_comments(production_log_id, problem_comment_id)` - Composite unique

### Check Constraints

- `positions.unit IN ('pcs', 'lmbr')`
- `production_logs.qty_output >= 0`
- `production_logs.qty_reject >= 0`
- `production_logs.problem_duration_minutes >= 0`
- `production_logs: (approved_spv IS NULL) OR (approved_coordinator = true)`

## 🔄 Business Rules

1. **Approval Flow**: Supervisor hanya bisa approve jika sudah di-approve oleh coordinator
2. **Unit Validation**: Position unit harus 'pcs' atau 'lmbr'
3. **Quantity Validation**: Qty output dan reject tidak boleh negatif
4. **Problem Duration**: Durasi kendala tidak boleh negatif
5. **Department Code**: Kode departemen unik per divisi
6. **Sub Position Code**: Kode sub posisi unik per posisi

## 📝 Usage

### Create Database

```sql
-- Run the SQL file
\i database_schema.sql
```

### Or using psql

```bash
psql -U username -d database_name -f database_schema.sql
```

### Or using Python/Alembic (Recommended)

```bash
# Run migrations
alembic upgrade head
```

## 🔍 Notes

- Database menggunakan PostgreSQL
- Semua timestamps menggunakan TIMESTAMP type
- Numeric values menggunakan NUMERIC(10,2) untuk presisi
- Production logs menggunakan BIGINT untuk ID (untuk menampung data besar)
- Password di workers menggunakan VARCHAR(255) untuk hash (bcrypt/argon2)

---

**Last Updated**: 2024-12-30
**Version**: 2.0 (includes password column)

