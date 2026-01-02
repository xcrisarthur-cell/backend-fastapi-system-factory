# Panduan Deployment ke Server Ubuntu

Berikut adalah langkah-langkah untuk men-deploy aplikasi FastAPI dan Database PostgreSQL ke server Ubuntu Anda.

**Target Konfigurasi:**
- API Backend berjalan di Port **1101** (http://103.164.99.2:1101)
- Website Frontend berjalan di Port **80** (http://103.164.99.2) - *Disiapkan terpisah*

## Prasyarat
File-file berikut sudah disiapkan di folder proyek:
- `Dockerfile` (Konfigurasi image aplikasi)
- `docker-compose.yml` (Orkestrasi aplikasi dan database)
- `nginx-mkp.conf` (Konfigurasi Reverse Proxy untuk API di port 1101)

## Langkah 1: Persiapan Server (Install Docker)
Masuk ke server via SSH dan jalankan perintah berikut untuk menginstall Docker:

```bash
# Update repository
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# Tambahkan GPG Key Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Tambahkan repository Docker
echo \
  "deb [arch=\"$(dpkg --print-architecture)\" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Cek instalasi
sudo docker run hello-world
```

## Langkah 2: Upload Project ke Server
Anda bisa menggunakan `git clone` (jika repo ini ada di GitHub/GitLab) atau `scp` dari komputer lokal Anda.

Contoh jika menggunakan SCP (jalankan dari komputer lokal):
```powershell
scp -P 2222 -r C:\Users\xcris\Documents\GitHub\backend-fastapi-system-factory server_mkp_bekasi@103.164.99.2:~/backend-fastapi
```

## Langkah 3: Jalankan Aplikasi Backend
Masuk ke folder project di server:
```bash
cd ~/backend-fastapi
```

Jalankan Docker Compose:
```bash
sudo docker compose up -d --build
```
Aplikasi backend sekarang berjalan di `localhost:8000` (internal server) dan belum bisa diakses publik.

## Langkah 4: Setup Database (Seeding)
Jalankan perintah ini untuk mengisi database dengan data awal (pastikan container sudah running):

```bash
sudo docker compose exec app python seed.py --yes
```

## Langkah 5: Setup Nginx (Agar API bisa diakses via Port 1101)
Kita akan mengkonfigurasi Nginx untuk mendengarkan port 1101 dan meneruskannya ke backend.

1. Install Nginx (jika belum ada):
   ```bash
   sudo apt install nginx
   ```

2. Copy konfigurasi Nginx yang sudah disiapkan:
   ```bash
   sudo cp nginx-mkp.conf /etc/nginx/sites-available/mkp_backend_api
   ```

3. Aktifkan konfigurasi:
   ```bash
   sudo ln -s /etc/nginx/sites-available/mkp_backend_api /etc/nginx/sites-enabled/
   ```
   *Catatan: Jangan hapus default config jika itu digunakan untuk frontend di port 80.*

4. Test dan Restart Nginx:
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

5. **PENTING: Buka Firewall (Jika ada)**
   Pastikan port 1101 dibuka di firewall server (UFW) atau Security Group penyedia cloud Anda.
   ```bash
   sudo ufw allow 1101/tcp
   ```

Sekarang akses API Backend di `http://103.164.99.2:1101/`.
Docs API ada di `http://103.164.99.2:1101/docs`.

Website frontend nantinya bisa dideploy terpisah di port 80.
