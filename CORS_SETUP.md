# 🔧 CORS Configuration Setup

Panduan untuk mengkonfigurasi CORS di backend FastAPI agar frontend dapat mengakses API.

## 📋 Masalah

Error CORS terjadi ketika frontend di Vercel/Netlify mencoba mengakses backend di Fly.io:
```
Access to XMLHttpRequest at 'https://backend-fastapi-system-factory.fly.dev/items' 
from origin 'https://mkp-operational.vercel.app' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## ✅ Solusi

Backend sudah dikonfigurasi untuk membaca allowed origins dari environment variable `ALLOWED_ORIGINS`. Anda perlu menambahkan origin frontend ke environment variable di Fly.io.

## 🚀 Setup CORS di Fly.io

### 1. Tambahkan Origin Vercel

```bash
# Set environment variable di Fly.io
fly secrets set ALLOWED_ORIGINS=https://mkp-operational.vercel.app
```

### 2. Jika Menggunakan Multiple Origins (Vercel + Netlify)

```bash
# Pisahkan dengan koma untuk multiple origins
fly secrets set ALLOWED_ORIGINS=https://mkp-operational.vercel.app,https://your-site.netlify.app
```

### 3. Jika Menggunakan Preview Deployments

Vercel dan Netlify membuat preview URLs untuk setiap branch/PR. Untuk mengizinkan semua preview deployments:

**Opsi A: Tambahkan Wildcard (Tidak Disarankan untuk Production)**
```python
# Modifikasi app/main.py untuk support wildcard
# Hanya untuk development/testing, jangan gunakan di production
```

**Opsi B: Tambahkan Preview URLs Secara Manual**
```bash
# Tambahkan preview URLs yang sering digunakan
fly secrets set ALLOWED_ORIGINS=https://mkp-operational.vercel.app,https://mkp-operational-git-main.vercel.app
```

**Opsi C: Gunakan Regex Pattern (Recommended)**
Modifikasi `app/main.py` untuk support pattern matching (lihat bagian Advanced Configuration)

### 4. Verifikasi

Setelah set environment variable, restart aplikasi:
```bash
fly apps restart backend-fastapi-system-factory
```

Atau deploy ulang:
```bash
fly deploy
```

## 🔍 Cek Konfigurasi Saat Ini

### Cek Environment Variables
```bash
fly secrets list
```

### Cek Logs untuk Allowed Origins
```bash
fly logs
# Cari baris: "CORS Allowed Origins: [...]"
```

### Test CORS
```bash
# Test dari command line
curl -H "Origin: https://mkp-operational.vercel.app" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://backend-fastapi-system-factory.fly.dev/items
```

Response harus mengandung:
```
Access-Control-Allow-Origin: https://mkp-operational.vercel.app
```

## 📝 Origins yang Sudah Terkonfigurasi

### Development (Selalu Diizinkan)
- `http://localhost:5173` (Vite default)
- `http://127.0.0.1:5173`
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:8080`
- `http://127.0.0.1:8080`
- `http://localhost:5174`
- `http://127.0.0.1:5174`

### Production (Perlu Ditambahkan via Environment Variable)
- `https://mkp-operational.vercel.app` ← **Perlu ditambahkan**
- `https://your-site.netlify.app` ← Jika menggunakan Netlify

## 🔧 Advanced Configuration

### Support Wildcard untuk Preview Deployments

Jika ingin mengizinkan semua preview deployments dari Vercel/Netlify, modifikasi `app/main.py`:

```python
import re
from fastapi.middleware.cors import CORSMiddleware

# ... existing code ...

# Add production origins from environment variable if set
if allowed_origins_env:
    production_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
    allowed_origins.extend(production_origins)
    
    # Support wildcard patterns (e.g., *.vercel.app)
    wildcard_origins = [origin for origin in production_origins if '*' in origin]
    for pattern in wildcard_origins:
        # Convert wildcard to regex
        regex_pattern = pattern.replace('.', r'\.').replace('*', r'.*')
        allowed_origins.append(regex_pattern)

# Remove duplicates while preserving order
allowed_origins = list(dict.fromkeys(allowed_origins))

# Custom CORS middleware untuk support regex
# Note: FastAPI CORSMiddleware tidak support regex langsung
# Perlu custom middleware atau gunakan allow_origin_regex
```

**Atau gunakan `allow_origin_regex`:**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Exact matches
    allow_origin_regex=r"https://.*\.vercel\.app",  # Regex for preview deployments
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)
```

## 🛠️ Troubleshooting

### CORS Masih Error Setelah Setup

1. **Cek Environment Variable**
   ```bash
   fly secrets list
   ```
   Pastikan `ALLOWED_ORIGINS` sudah diset dengan benar.

2. **Restart Aplikasi**
   ```bash
   fly apps restart backend-fastapi-system-factory
   ```

3. **Cek Logs**
   ```bash
   fly logs
   ```
   Cari baris "CORS Allowed Origins" untuk memastikan origin sudah terdaftar.

4. **Cek Browser Console**
   - Buka browser DevTools → Network tab
   - Cek request ke API
   - Lihat response headers, pastikan ada `Access-Control-Allow-Origin`

5. **Test dengan curl**
   ```bash
   curl -v -H "Origin: https://mkp-operational.vercel.app" \
        https://backend-fastapi-system-factory.fly.dev/items
   ```

### Origin Tidak Terdaftar

- Pastikan tidak ada typo di URL
- Pastikan menggunakan HTTPS (bukan HTTP) untuk production
- Pastikan tidak ada trailing slash di URL
- Restart aplikasi setelah set environment variable

## 📚 Referensi

- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [Fly.io Secrets Documentation](https://fly.io/docs/reference/secrets/)
- [Vercel Preview Deployments](https://vercel.com/docs/concepts/deployments/preview-deployments)

