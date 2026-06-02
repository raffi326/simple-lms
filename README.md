# 🎓 Simple LMS (Learning Management System)

Simple LMS adalah aplikasi backend untuk sistem manajemen pembelajaran yang tangguh, dibangun menggunakan **Django Ninja** dan **PostgreSQL**, serta ditingkatkan dengan **Redis**, **MongoDB**, dan **Celery**. Proyek ini sepenuhnya dikontainerisasi menggunakan **Docker**.

---

## 🚀 Fitur Utama

- **Manajemen Course**: CRUD Matakuliah, Konten, dan Anggota Kelas.
- **Redis Caching**: Caching pada endpoint list dan detail course untuk performa tinggi.
- **Rate Limiting**: Pembatasan akses (60 requests/minute) untuk menjaga stabilitas API.
- **MongoDB Logging**: Pencatatan Activity Logs dan Learning Analytics secara real-time.
- **Asynchronous Tasks**: Pemrosesan background tasks menggunakan Celery & RabbitMQ:
  - Pengiriman email pendaftaran otomatis.
  - Pembuatan sertifikat saat course selesai.
  - Ekspor laporan course ke CSV secara async.
  - Pembaruan statistik berkala via Celery Beat.
- **Monitoring**: Dashboard Flower untuk memantau status antrian task.

---

## 🛠️ Teknologi yang Digunakan

- **Backend**: Python 3.11, Django 5, Django Ninja
- **Database**: PostgreSQL 15 (Relational Data)
- **NoSQL**: 
  - **Redis 7**: Caching & Rate Limiting backend.
  - **MongoDB 6**: Document storage untuk logs & analytics.
- **Message Broker**: RabbitMQ (Task Queue)
- **Task Runner**: Celery & Celery Beat
- **Containerization**: Docker & Docker Compose

---

## 📦 Struktur Project

```
simple-lms/
│── code/
│   ├── core/           # Logic inti, auth, ratelimit, mongodb
│   ├── courses/        # Manajemen data matakuliah & tasks
│   ├── lms/            # Konfigurasi project & celery setup
│   └── manage.py
│── config/             # Konfigurasi tambahan
│── docker-compose.yml
│── Dockerfile
│── requirements.txt
└── DOCUMENTATION.md    # Detail arsitektur & strategi teknis
```

---

## ⚙️ Cara Menjalankan Project

### 1. Persiapan Environment
Salin file `.env.example` menjadi `.env` dan sesuaikan konfigurasinya:
```bash
cp .env.example .env
```

### 2. Jalankan Docker Compose
```bash
docker compose up --build
```

### 3. Inisialisasi Database
Jalankan migrasi database di dalam container Django:
```bash
docker exec -it django_app python manage.py migrate
```

### 4. Buat Akun Admin
```bash
docker exec -it django_app python manage.py createsuperuser
```

---

## 🔗 Akses Aplikasi & Monitoring

- **API Documentation (Swagger)**: [http://localhost:8000/api/v1/docs]
- **Django Admin**: [http://localhost:8000/admin]
- **Celery Monitoring (Flower)**: [http://localhost:5555]
- **RabbitMQ Management**: [http://localhost:15672]

---

## 🐳 Perintah Penting Docker

| Perintah | Fungsi |
|--------|--------|
| `docker compose up -d` | Menjalankan semua layanan di background |
| `docker compose down` | Menghentikan semua layanan |
| `docker compose logs -f web` | Melihat log aplikasi Django |
| `docker compose logs -f celery-worker` | Melihat log proses background task |

---

## 📌 Dokumentasi Teknis
Untuk detail mengenai arsitektur sistem, strategi caching, alur task, dan perintah CLI Redis/MongoDB, silakan merujuk ke [DOCUMENTATION.md](DOCUMENTATION.md).

---

## ⚠️ Catatan Pengembangan
- Pastikan port 8000, 5555, 5672, 6379, dan 27017 tidak digunakan oleh aplikasi lain.
- Gunakan koleksi Postman yang tersedia di root project untuk testing endpoint.
