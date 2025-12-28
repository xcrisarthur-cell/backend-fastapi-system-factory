# MKP Operational API - Postman Collection

## 📋 Deskripsi

Collection Postman lengkap untuk testing semua endpoint API MKP Operational System. Collection ini mencakup semua CRUD operations untuk semua tabel dalam database.

## 🚀 Cara Menggunakan

### 1. Import Collection ke Postman

1. Buka Postman
2. Klik **Import** di pojok kiri atas
3. Pilih file `MKP_Operational_API_Collection.postman_collection.json`
4. Klik **Import**

### 2. Import Environment (Opsional)

1. Klik **Environments** di sidebar kiri
2. Klik **Import**
3. Pilih file `MKP_Operational_API_Environment.postman_environment.json`
4. Klik **Import**
5. Pilih environment **MKP Operational API - Local** di dropdown environment

### 3. Konfigurasi Base URL

Jika tidak menggunakan environment, Anda bisa mengubah base URL secara manual:
- Collection variable: `{{base_url}}` (default: `http://localhost:8000`)
- Atau ubah langsung di setiap request

## 📁 Struktur Collection

Collection diorganisir dalam folder sesuai dengan resource:

### 1. **Divisions** (5 endpoints)
- GET `/divisions` - Get all divisions
- GET `/divisions/{id}` - Get division by ID
- POST `/divisions` - Create division
- PUT `/divisions/{id}` - Update division
- DELETE `/divisions/{id}` - Delete division

### 2. **Departments** (6 endpoints)
- GET `/departments` - Get all departments (with division info)
- GET `/departments/{id}` - Get department by ID
- GET `/departments/by-division/{division_id}` - Get departments by division
- POST `/departments` - Create department
- PUT `/departments/{id}` - Update department
- DELETE `/departments/{id}` - Delete department

### 3. **Positions** (5 endpoints)
- GET `/positions` - Get all positions
- GET `/positions/{id}` - Get position by ID
- POST `/positions` - Create position (unit: "pcs" or "lmbr")
- PUT `/positions/{id}` - Update position
- DELETE `/positions/{id}` - Delete position

### 4. **Sub Positions** (6 endpoints)
- GET `/sub-positions` - Get all sub positions (with position info)
- GET `/sub-positions/{id}` - Get sub position by ID
- GET `/sub-positions/by-position/{position_id}` - Get sub positions by position
- POST `/sub-positions` - Create sub position
- PUT `/sub-positions/{id}` - Update sub position
- DELETE `/sub-positions/{id}` - Delete sub position

### 5. **Workers** (5 endpoints)
- GET `/workers` - Get all workers (with position & department info)
- GET `/workers/{id}` - Get worker by ID
- POST `/workers` - Create worker
- PUT `/workers/{id}` - Update worker
- DELETE `/workers/{id}` - Delete worker

### 6. **Shifts** (5 endpoints)
- GET `/shifts` - Get all shifts
- GET `/shifts/{id}` - Get shift by ID
- POST `/shifts` - Create shift
- PUT `/shifts/{id}` - Update shift
- DELETE `/shifts/{id}` - Delete shift

### 7. **Suppliers** (5 endpoints)
- GET `/suppliers` - Get all suppliers
- GET `/suppliers/{id}` - Get supplier by ID
- POST `/suppliers` - Create supplier
- PUT `/suppliers/{id}` - Update supplier
- DELETE `/suppliers/{id}` - Delete supplier

### 8. **Items** (6 endpoints)
- GET `/items` - Get all items
- GET `/items/{id}` - Get item by ID
- GET `/items/number/{item_number}` - Get item by item number
- POST `/items` - Create item
- PUT `/items/{id}` - Update item
- DELETE `/items/{id}` - Delete item

### 9. **Problem Comments** (5 endpoints)
- GET `/problem-comments` - Get all problem comments
- GET `/problem-comments/{id}` - Get problem comment by ID
- POST `/problem-comments` - Create problem comment
- PUT `/problem-comments/{id}` - Update problem comment
- DELETE `/problem-comments/{id}` - Delete problem comment

### 10. **Production Logs** (7 endpoints)
- GET `/production-logs` - Get all production logs (with all related data)
- GET `/production-logs/{id}` - Get production log by ID
- POST `/production-logs` - Create production log
- PUT `/production-logs/{id}` - Update production log
- PUT `/production-logs/{id}` - Approve by coordinator
- PUT `/production-logs/{id}` - Approve by SPV
- DELETE `/production-logs/{id}` - Delete production log

## 🔑 Fitur Khusus

### Nested Relationships
Semua GET endpoints mengembalikan data dengan nested relationships:
- **Workers** → includes `position` dan `department` (dengan `division`)
- **Departments** → includes `division`
- **Sub Positions** → includes `position`
- **Production Logs** → includes semua relasi (worker, position, department, shift, supplier, item, problem_comments)

### Production Logs - Many-to-Many
Production logs menggunakan `problem_comment_ids` array untuk many-to-many relationship dengan problem comments.

### Approval System
Production logs memiliki sistem approval:
- `approved_coordinator` - Approval oleh coordinator
- `approved_spv` - Approval oleh SPV (harus coordinator approve dulu)

## 📝 Contoh Request Body

### Create Worker
```json
{
    "name": "John Doe",
    "position_id": 1,
    "department_id": 1
}
```

### Create Production Log
```json
{
    "worker_id": 1,
    "position_id": 1,
    "sub_position_id": 1,
    "shift_id": 1,
    "supplier_id": 1,
    "item_id": 1,
    "qty_output": 100.50,
    "qty_reject": 5.25,
    "problem_duration_minutes": 30,
    "problem_comment_ids": [1, 2]
}
```

### Approve Production Log
```json
{
    "approved_coordinator": true,
    "approved_coordinator_by": 1
}
```

## ⚠️ Catatan Penting

1. **Foreign Key Validation**: Pastikan ID yang digunakan sudah ada di database sebelum membuat relasi
2. **Unique Constraints**: 
   - Division: `code` dan `name` harus unique
   - Department: `code` harus unique per division
   - Position: `code` harus unique, `unit` harus "pcs" atau "lmbr"
   - Sub Position: `code` harus unique per position
   - Worker: tidak ada unique constraint
   - Shift: `name` harus unique
   - Supplier: `name` harus unique
   - Item: `item_number` harus unique
   - Problem Comment: `description` harus unique

3. **Order of Creation**: Disarankan membuat data dalam urutan:
   1. Divisions
   2. Departments
   3. Positions
   4. Sub Positions
   5. Workers
   6. Shifts
   7. Suppliers
   8. Items
   9. Problem Comments
   10. Production Logs

## 🐛 Troubleshooting

### Error 404
- Pastikan ID yang digunakan sudah ada di database
- Pastikan endpoint URL benar

### Error 400
- Cek unique constraints
- Cek format data (unit harus "pcs" atau "lmbr")
- Cek foreign key references

### Error 500
- Pastikan database connection berjalan
- Cek server logs untuk detail error

## 📚 Dokumentasi API

Untuk dokumentasi API lengkap, buka:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔄 Update Collection

Jika ada perubahan endpoint, update collection dengan:
1. Export collection dari Postman
2. Replace file `MKP_Operational_API_Collection.postman_collection.json`
3. Commit perubahan ke repository

---

**Happy Testing! 🚀**
