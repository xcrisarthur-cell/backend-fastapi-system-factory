# Postman Collection - MKP Operational API

Collection Postman untuk testing semua endpoint API MKP Operational.

## File yang Tersedia

1. **MKP_Operational_API.postman_collection.json** - Collection utama dengan semua endpoint
2. **MKP_Operational_API.postman_environment.json** - Environment file untuk konfigurasi base URL

## Cara Menggunakan

### 1. Import Collection ke Postman

1. Buka Postman
2. Klik **Import** di pojok kiri atas
3. Pilih file **MKP_Operational_API.postman_collection.json**
4. Klik **Import**

### 2. Import Environment (Opsional)

1. Klik **Import** di Postman
2. Pilih file **MKP_Operational_API.postman_environment.json**
3. Klik **Import**
4. Pilih environment **MKP Operational API - Local** di dropdown environment (pojok kanan atas)
5. Pastikan base_url sudah di-set ke `http://localhost:8000` (atau sesuaikan dengan server Anda)

### 3. Menjalankan Server API

Pastikan server FastAPI sudah berjalan:

```bash
uvicorn app.main:app --reload
```

Server akan berjalan di `http://localhost:8000` (default)

### 4. Testing Endpoints

Collection ini terorganisir dalam folder berdasarkan resource:

#### **Workers** (5 endpoints)
- ✅ GET All Workers
- ✅ GET Worker by ID
- ✅ POST Create Worker
- ✅ PUT Update Worker
- ✅ DELETE Worker

#### **Positions** (5 endpoints)
- ✅ GET All Positions
- ✅ GET Position by ID
- ✅ POST Create Position
- ✅ PUT Update Position
- ✅ DELETE Position

**Catatan:** Unit harus `"pcs"` atau `"lmbr"`

#### **Sub Positions** (6 endpoints)
- ✅ GET All Sub Positions
- ✅ GET Sub Position by ID
- ✅ GET Sub Positions by Position ID
- ✅ POST Create Sub Position
- ✅ PUT Update Sub Position
- ✅ DELETE Sub Position

#### **Shifts** (5 endpoints)
- ✅ GET All Shifts
- ✅ GET Shift by ID
- ✅ POST Create Shift
- ✅ PUT Update Shift
- ✅ DELETE Shift

#### **Suppliers** (5 endpoints)
- ✅ GET All Suppliers
- ✅ GET Supplier by ID
- ✅ POST Create Supplier
- ✅ PUT Update Supplier
- ✅ DELETE Supplier

#### **Items** (5 endpoints)
- ✅ GET All Items
- ✅ GET Item by Item Number
- ✅ POST Create Item
- ✅ PUT Update Item
- ✅ DELETE Item

**Catatan:** Item menggunakan `item_number` sebagai identifier, bukan `id`

#### **Problem Comments** (5 endpoints)
- ✅ GET All Problem Comments
- ✅ GET Problem Comment by ID
- ✅ POST Create Problem Comment
- ✅ PUT Update Problem Comment
- ✅ DELETE Problem Comment

#### **Production Logs** (6 endpoints)
- ✅ GET All Production Logs
- ✅ GET Production Log by ID
- ✅ POST Create Production Log
- ✅ POST Create Production Log with Problem
- ✅ PUT Update Production Log
- ✅ DELETE Production Log

## Urutan Testing yang Disarankan

Karena ada relasi foreign key, disarankan untuk membuat data dalam urutan berikut:

1. **Workers** - Buat worker terlebih dahulu
2. **Positions** - Buat position
3. **Sub Positions** - Membutuhkan position_id
4. **Shifts** - Buat shift
5. **Suppliers** - Buat supplier
6. **Items** - Buat item
7. **Problem Comments** - Buat problem comment (opsional)
8. **Production Logs** - Membutuhkan semua ID di atas

## Contoh Request Body

### Create Position
```json
{
    "code": "POS001",
    "unit": "pcs"
}
```

### Create Sub Position
```json
{
    "position_id": 1,
    "code": "SUB001"
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
    "problem_comment_id": null,
    "problem_duration_minutes": null
}
```

## Tips

1. **Gunakan Environment Variables**: Ubah `base_url` di environment jika server berjalan di port/domain berbeda
2. **Update ID**: Setelah membuat data baru, update ID di request berikutnya sesuai dengan response yang diterima
3. **Test Error Cases**: Coba request dengan ID yang tidak ada untuk test error handling (404)
4. **Test Validation**: Coba create dengan data duplikat untuk test validation (400)

## Response Codes

- **200 OK** - Request berhasil
- **201 Created** - Resource berhasil dibuat (POST)
- **400 Bad Request** - Validasi gagal atau data duplikat
- **404 Not Found** - Resource tidak ditemukan
- **422 Unprocessable Entity** - Request body tidak valid

## Dokumentasi API

Setelah server berjalan, dokumentasi API tersedia di:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc








