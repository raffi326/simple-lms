# 🎓 Simple LMS (Learning Management System)

Simple LMS adalah aplikasi berbasis web yang dibangun menggunakan **Django** dan **PostgreSQL**, serta dijalankan menggunakan **Docker** untuk mempermudah deployment dan development.

---

## 🚀 Fitur Utama

- Manajemen Course (Tambah, Edit, Hapus)
- Upload gambar course
- Admin panel Django
- Database PostgreSQL
- Containerized dengan Docker

---

## 🛠️ Teknologi yang Digunakan

- Python 3.11
- Django 5
- PostgreSQL 15
- Docker & Docker Compose
- Pillow (untuk ImageField)

---

## 📦 Struktur Project

```
simple-lms/
│── code/
│   ├── manage.py
│   ├── lms/
│   └── courses/
│── docker-compose.yml
│── Dockerfile
│── requirements.txt
```

---

## ⚙️ Cara Menjalankan Project

### 1. Clone Repository
```bash
git clone https://github.com/raffi326/simple-lms.git
cd simple-lms
```

### 2. Jalankan Docker
```bash
docker compose up --build
```

### 3. Jalankan Migration
```bash
docker exec -it django_app python code/manage.py migrate
```

### 4. Buat Superuser
```bash
docker exec -it django_app python code/manage.py createsuperuser
```

### 5. Akses Aplikasi

- Website: http://localhost:8000  
- Admin: http://localhost:8000/admin  

---

## 🐳 Perintah Penting Docker

| Perintah | Fungsi |
|--------|--------|
| `docker compose up -d` | Menjalankan container di background |
| `docker compose down` | Menghentikan container |
| `docker ps` | Melihat container aktif |
| `docker logs django_app` | Melihat log Django |

---

## ⚠️ Catatan

- Pastikan Docker sudah terinstall
- Jalankan migrate sebelum menggunakan aplikasi
- Gunakan port 8000 untuk akses aplikasi

---

## 📌 Status Project

✅ Development berjalan  
✅ Docker setup berhasil  
✅ Database terhubung  
🚧 Masih dalam pengembangan

---


