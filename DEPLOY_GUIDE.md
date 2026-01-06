# Panduan Deployment ke Server Ubuntu

Panduan ini menjelaskan cara men-deploy aplikasi backend ke server Ubuntu dan melakukan update di masa mendatang.

## Persiapan Server (Sekali Saja)

1.  **Install Python & Git:**
    Pastikan Python 3.10+ dan Git sudah terinstall.
    ```bash
    sudo apt update
    sudo apt install python3-pip python3-venv git -y
    ```

2.  **Clone Repository:**
    Lakukan clone manual seperti yang Anda minta.
    ```bash
    git clone https://github.com/username/backend-fastapi-system-factory.git
    cd backend-fastapi-system-factory
    ```

3.  **Setup Virtual Environment:**
    Disarankan menggunakan virtual environment agar package tidak tercampur.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Konfigurasi Environment:**
    Buat file `.env` dari contoh yang ada.
    ```bash
    cp .env.example .env
    nano .env
    ```
    Isi `DATABASE_URL` dengan koneksi PostgreSQL Anda.

5.  **Beri Izin Eksekusi Script Deploy:**
    ```bash
    chmod +x deploy.sh
    ```

---

## 1. Deployment Pertama Kali (Setup)

Gunakan perintah ini saat pertama kali deploy. **PERHATIAN: Perintah ini akan menghapus database lama (jika ada) dan mengisinya dengan data awal (seeder).**

```bash
./deploy.sh setup
```

Proses yang terjadi:
1.  Install dependencies (`pip install`).
2.  Reset Database (Drop & Create Schema).
3.  Jalankan Migration.
4.  Jalankan Seeder (isi data awal).

---

## 2. Update Aplikasi (Rutin)

Gunakan perintah ini jika ada update di GitHub (misal: penambahan kolom baru di tabel). **Perintah ini AMAN untuk data yang sudah ada.**

```bash
./deploy.sh update
```

Proses yang terjadi:
1.  `git pull` (mengambil kode terbaru).
2.  Install dependencies baru (jika ada).
3.  `alembic upgrade head` (update struktur tabel database tanpa menghapus data).
    *   Kolom baru akan ditambahkan.
    *   Kolom yang dihapus akan hilang.
    *   Data lama tetap aman.

---

## Catatan Penting

*   **Proses Development (Di Laptop Anda):**
    Setiap kali Anda mengubah struktur database (misal: tambah kolom di `models.py`), lakukan langkah ini sebelum push ke GitHub:
    1.  Jalankan: `alembic revision --autogenerate -m "pesan perubahan"`
    2.  File migrasi baru akan muncul di folder `alembic/versions/`.
    3.  Commit dan Push file tersebut beserta perubahan kode Anda ke GitHub.

*   **Migration Otomatis di Server:**
    Saat Anda menjalankan `./deploy.sh update` di server, sistem akan membaca file migrasi yang baru Anda push tadi dan menjalankannya (`alembic upgrade head`). Ini memastikan database server sinkron dengan kode tanpa kehilangan data.

*   **Virtual Environment:** Pastikan Anda selalu mengaktifkan virtual environment (`source venv/bin/activate`) sebelum menjalankan script deploy.
