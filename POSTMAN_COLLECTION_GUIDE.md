# 📮 Postman Collection Guide

Panduan lengkap untuk menggunakan Postman Collection API MKP Operational System Factory.

## 📦 File yang Tersedia

1. **MKP_Operational_API_Complete.postman_collection.json** - Complete API collection
2. **MKP_Operational_API_Environment.postman_environment.json** - Environment file untuk production

## 🚀 Cara Import ke Postman

### 1. Import Collection

1. Buka Postman
2. Klik **Import** (di kiri atas)
3. Pilih file `MKP_Operational_API_Complete.postman_collection.json`
4. Klik **Import**

### 2. Import Environment (Optional)

1. Klik **Import** lagi
2. Pilih file `MKP_Operational_API_Environment.postman_environment.json`
3. Klik **Import**
4. Pilih environment "MKP Operational API - Production" di dropdown environment (kanan atas)

## 📋 Struktur Collection

Collection terorganisir dalam folder-folder berikut:

### 1. **Health Check**
   - `GET /health` - Check API health status

### 2. **Workers**
   - `POST /workers/login` - Login worker
   - `GET /workers` - Get all workers
   - `GET /workers/:worker_id` - Get worker by ID
   - `POST /workers` - Create worker
   - `PUT /workers/:worker_id` - Update worker
   - `DELETE /workers/:worker_id` - Delete worker

### 3. **Items**
   - `GET /items` - Get all items
   - `GET /items/:item_identifier` - Get item by ID or number
   - `GET /items/number/:item_number` - Get item by number
   - `POST /items` - Create item
   - `PUT /items/:item_id` - Update item
   - `DELETE /items/:item_id` - Delete item

### 4. **Positions**
   - `GET /positions` - Get all positions
   - `GET /positions/:position_id` - Get position by ID
   - `POST /positions` - Create position
   - `PUT /positions/:position_id` - Update position
   - `DELETE /positions/:position_id` - Delete position

### 5. **Sub Positions**
   - `GET /sub-positions` - Get all sub positions
   - `GET /sub-positions/:sub_position_id` - Get sub position by ID
   - `GET /sub-positions/by-position/:position_id` - Get sub positions by position ID
   - `POST /sub-positions` - Create sub position
   - `PUT /sub-positions/:sub_position_id` - Update sub position
   - `DELETE /sub-positions/:sub_position_id` - Delete sub position

### 6. **Shifts**
   - `GET /shifts` - Get all shifts
   - `GET /shifts/:shift_id` - Get shift by ID
   - `POST /shifts` - Create shift
   - `PUT /shifts/:shift_id` - Update shift
   - `DELETE /shifts/:shift_id` - Delete shift

### 7. **Suppliers**
   - `GET /suppliers` - Get all suppliers
   - `GET /suppliers/:supplier_id` - Get supplier by ID
   - `POST /suppliers` - Create supplier
   - `PUT /suppliers/:supplier_id` - Update supplier
   - `DELETE /suppliers/:supplier_id` - Delete supplier

### 8. **Divisions**
   - `GET /divisions` - Get all divisions
   - `GET /divisions/:division_id` - Get division by ID
   - `POST /divisions` - Create division
   - `PUT /divisions/:division_id` - Update division
   - `DELETE /divisions/:division_id` - Delete division

### 9. **Departments**
   - `GET /departments` - Get all departments
   - `GET /departments/:department_id` - Get department by ID
   - `GET /departments/by-division/:division_id` - Get departments by division ID
   - `POST /departments` - Create department
   - `PUT /departments/:department_id` - Update department
   - `DELETE /departments/:department_id` - Delete department

### 10. **Problem Comments**
   - `GET /problem-comments` - Get all problem comments
   - `GET /problem-comments/:comment_id` - Get problem comment by ID
   - `POST /problem-comments` - Create problem comment
   - `PUT /problem-comments/:comment_id` - Update problem comment
   - `DELETE /problem-comments/:comment_id` - Delete problem comment

### 11. **Production Logs**
   - `GET /production-logs` - Get all production logs
   - `GET /production-logs/:log_id` - Get production log by ID
   - `POST /production-logs` - Create production log
   - `PUT /production-logs/:log_id` - Update production log
   - `DELETE /production-logs/:log_id` - Delete production log

## 🔧 Konfigurasi

### Base URL

Collection menggunakan variable `{{base_url}}` yang default-nya:
- **Production**: `https://backend-fastapi-system-factory.fly.dev`

### Mengubah Base URL

1. Klik collection name → **Variables** tab
2. Edit value `base_url` sesuai kebutuhan
3. Atau gunakan environment file untuk multiple environments

### Environment Variables

Jika ingin menggunakan environment yang berbeda:

1. Buat environment baru di Postman
2. Set variable `base_url`:
   - Production: `https://backend-fastapi-system-factory.fly.dev`
   - Development: `http://localhost:8000`
3. Pilih environment di dropdown (kanan atas)

## 📝 Contoh Request Body

### Create Production Log

```json
{
    "worker_id": 1,
    "position_id": 1,
    "sub_position_id": null,
    "shift_id": 1,
    "supplier_id": null,
    "item_id": 1,
    "qty_output": 100.0,
    "qty_reject": 5.0,
    "problem_duration_minutes": null,
    "problem_comment_ids": [1, 2]
}
```

### Create Worker

```json
{
    "name": "John Doe",
    "position_id": 1,
    "department_id": 1,
    "password": "password123"
}
```

### Update Production Log (Approval)

```json
{
    "approved_coordinator": true,
    "approved_coordinator_by": 2,
    "approved_spv": true,
    "approved_spv_by": 3
}
```

## 🧪 Testing

### Pre-request Scripts

Anda bisa menambahkan pre-request scripts untuk:
- Set dynamic values
- Generate tokens
- Set headers

### Tests

Collection sudah siap untuk ditambahkan test scripts. Contoh:

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has data", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('array');
});
```

## 📚 Tips

1. **Save Responses**: Klik "Save Response" untuk menyimpan contoh response
2. **Duplicate Request**: Klik kanan request → Duplicate untuk membuat variasi
3. **Use Variables**: Gunakan `{{variable_name}}` untuk dynamic values
4. **Organize**: Buat folder baru untuk grouping requests yang sering digunakan
5. **Documentation**: Setiap request sudah memiliki description

## 🔄 Update Collection

Jika ada perubahan API:
1. Update collection file
2. Re-import ke Postman
3. Atau edit langsung di Postman dan export ulang

## 📞 Support

Jika ada pertanyaan atau masalah:
1. Cek API documentation di `/docs` endpoint (Swagger UI)
2. Cek response error untuk detail
3. Pastikan base_url sudah benar
4. Pastikan CORS sudah dikonfigurasi jika testing dari browser









