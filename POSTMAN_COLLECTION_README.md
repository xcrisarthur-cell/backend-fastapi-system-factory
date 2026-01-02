# Postman Collection - MKP Operational API

Koleksi lengkap untuk testing semua endpoint API MKP Operational System Factory.

## 📦 File yang Tersedia

1. **MKP_Operational_API_Collection.postman_collection.json** - Collection lengkap dengan semua endpoint
2. **MKP_Operational_API_Local.postman_environment.json** - Environment untuk local development
3. **MKP_Operational_API_Production.postman_environment.json** - Environment untuk production

## 🚀 Cara Menggunakan

### 1. Import Collection dan Environment ke Postman

1. Buka Postman
2. Klik **Import** di pojok kiri atas
3. Pilih file-file berikut:
   - `MKP_Operational_API_Collection.postman_collection.json`
   - `MKP_Operational_API_Local.postman_environment.json`
   - `MKP_Operational_API_Production.postman_environment.json`

### 2. Pilih Environment

Di pojok kanan atas Postman, pilih environment yang ingin digunakan:
- **MKP Operational API - Local** untuk testing di localhost
- **MKP Operational API - Production** untuk testing di production

### 3. Mulai Testing

Collection sudah terorganisir berdasarkan resource:
- Health Check
- Workers (Login, CRUD)
- Divisions (CRUD)
- Departments (CRUD + Get by Division)
- Positions (CRUD)
- Sub Positions (CRUD + Get by Position)
- Shifts (CRUD)
- Suppliers (CRUD)
- Items (CRUD + Get by Number)
- Problem Comments (CRUD)
- Production Logs (CRUD + Approval)

## 📋 Endpoint yang Tersedia

### Health Check
- `GET /health` - Check API status

### Workers
- `POST /workers/login` - Login worker
- `GET /workers` - Get all workers
- `GET /workers/:worker_id` - Get worker by ID
- `POST /workers/` - Create worker
- `PUT /workers/:worker_id` - Update worker
- `DELETE /workers/:worker_id` - Delete worker

### Divisions
- `GET /divisions` - Get all divisions
- `GET /divisions/:division_id` - Get division by ID
- `POST /divisions/` - Create division
- `PUT /divisions/:division_id` - Update division
- `DELETE /divisions/:division_id` - Delete division

### Departments
- `GET /departments` - Get all departments
- `GET /departments/:department_id` - Get department by ID
- `GET /departments/by-division/:division_id` - Get departments by division
- `POST /departments/` - Create department
- `PUT /departments/:department_id` - Update department
- `DELETE /departments/:department_id` - Delete department

### Positions
- `GET /positions` - Get all positions
- `GET /positions/:position_id` - Get position by ID
- `POST /positions/` - Create position
- `PUT /positions/:position_id` - Update position
- `DELETE /positions/:position_id` - Delete position

### Sub Positions
- `GET /sub-positions` - Get all sub positions
- `GET /sub-positions/:sub_position_id` - Get sub position by ID
- `GET /sub-positions/by-position/:position_id` - Get sub positions by position
- `POST /sub-positions/` - Create sub position
- `PUT /sub-positions/:sub_position_id` - Update sub position
- `DELETE /sub-positions/:sub_position_id` - Delete sub position

### Shifts
- `GET /shifts` - Get all shifts
- `GET /shifts/:shift_id` - Get shift by ID
- `POST /shifts/` - Create shift
- `PUT /shifts/:shift_id` - Update shift
- `DELETE /shifts/:shift_id` - Delete shift

### Suppliers
- `GET /suppliers` - Get all suppliers
- `GET /suppliers/:supplier_id` - Get supplier by ID
- `POST /suppliers/` - Create supplier
- `PUT /suppliers/:supplier_id` - Update supplier
- `DELETE /suppliers/:supplier_id` - Delete supplier

### Items
- `GET /items` - Get all items
- `GET /items/:item_identifier` - Get item by ID or item number
- `GET /items/number/:item_number` - Get item by item number
- `POST /items/` - Create item
- `PUT /items/:item_id` - Update item
- `DELETE /items/:item_id` - Delete item

### Problem Comments
- `GET /problem-comments` - Get all problem comments
- `GET /problem-comments/:comment_id` - Get problem comment by ID
- `POST /problem-comments/` - Create problem comment
- `PUT /problem-comments/:comment_id` - Update problem comment
- `DELETE /problem-comments/:comment_id` - Delete problem comment

### Production Logs
- `GET /production-logs` - Get all production logs
- `GET /production-logs/:log_id` - Get production log by ID
- `POST /production-logs/` - Create production log
- `POST /production-logs/` (with problem) - Create production log with problem comments
- `PUT /production-logs/:log_id` - Update production log
- `PUT /production-logs/:log_id` (approve coordinator) - Approve by coordinator
- `PUT /production-logs/:log_id` (approve supervisor) - Approve by supervisor
- `DELETE /production-logs/:log_id` - Delete production log

## 🔐 Test Credentials (dari seeder)

Setelah menjalankan seeder, Anda dapat menggunakan credentials berikut untuk testing:

### Koordinator
- Worker ID: 31
- Password: `zaenal1`

### Supervisor
- Worker ID: 32
- Password: `prido1`

### Admin Produksi
- Worker ID: 33
- Password: `kiky1`
- Worker ID: 34
- Password: `rino1`

### Superadmin
- Worker ID: 35
- Password: `mas5indo`

## 💡 Tips

1. **Update Variable Values**: Sebelum testing, pastikan untuk mengupdate nilai variable di request (seperti `:worker_id`, `:division_id`, dll) dengan ID yang valid dari database Anda.

2. **Test Flow**: Disarankan untuk test dalam urutan:
   - Health Check
   - Get All untuk setiap resource (untuk melihat data yang ada)
   - Create untuk membuat data baru
   - Update untuk mengupdate data
   - Delete untuk menghapus data (hati-hati!)

3. **Production Logs**: Untuk membuat production log, pastikan semua foreign key (worker_id, position_id, shift_id, item_id) sudah ada di database.

4. **Approval Flow**: 
   - Production log harus di-approve oleh coordinator terlebih dahulu
   - Setelah itu baru bisa di-approve oleh supervisor

## 🔄 Environment Variables

Collection menggunakan variable `{{base_url}}` yang akan otomatis diisi berdasarkan environment yang dipilih:

- **Local**: `http://127.0.0.1:8000`
- **Production**: `https://backend-fastapi-system-factory.fly.dev`

## 📝 Notes

- Semua request menggunakan `Content-Type: application/json` untuk POST dan PUT
- Response akan dalam format JSON
- Error response akan mengikuti format FastAPI standard

## 🐛 Troubleshooting

### Error: "Cannot connect to server"
- Pastikan backend server sudah running
- Check apakah base_url di environment sudah benar
- Untuk local, pastikan server berjalan di port 8000

### Error: "404 Not Found"
- Pastikan endpoint path sudah benar
- Check apakah resource dengan ID tersebut ada di database

### Error: "400 Bad Request"
- Check request body, pastikan format JSON sudah benar
- Pastikan semua required fields sudah diisi
- Check apakah ada constraint violation (duplicate code, etc.)

---

**Happy Testing! 🚀**
