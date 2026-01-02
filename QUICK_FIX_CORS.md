# ⚡ Quick Fix - CORS Error

## 🚨 Error yang Terjadi

```
Access to XMLHttpRequest at 'https://backend-fastapi-system-factory.fly.dev/items' 
from origin 'https://mkp-operational.vercel.app' has been blocked by CORS policy
```

## ✅ Solusi Cepat

### Langkah 1: Set Environment Variable di Fly.io

```bash
fly secrets set ALLOWED_ORIGINS=https://mkp-operational.vercel.app
```

### Langkah 2: Restart Aplikasi

```bash
fly apps restart backend-fastapi-system-factory
```

### Langkah 3: Verifikasi

Buka browser console di `https://mkp-operational.vercel.app` dan cek apakah error CORS sudah hilang.

## 🔍 Jika Masih Error

1. **Cek apakah environment variable sudah diset:**
   ```bash
   fly secrets list
   ```

2. **Cek logs untuk melihat allowed origins:**
   ```bash
   fly logs | grep "CORS Allowed Origins"
   ```

3. **Pastikan URL benar (tanpa trailing slash):**
   - ✅ `https://mkp-operational.vercel.app`
   - ❌ `https://mkp-operational.vercel.app/`

## 📝 Catatan

- Backend sudah dikonfigurasi untuk support Vercel preview deployments (semua `*.vercel.app`)
- Jika menggunakan Netlify, tambahkan juga: `https://your-site.netlify.app`
- Untuk multiple origins, pisahkan dengan koma: `origin1,origin2,origin3`

## 📚 Dokumentasi Lengkap

Lihat `CORS_SETUP.md` untuk dokumentasi lengkap dan advanced configuration.






