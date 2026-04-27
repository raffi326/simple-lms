# Progress 3: Simple LMS - REST API & Authentication System

## Overview

REST API lengkap untuk Simple Learning Management System menggunakan Django Ninja dengan JWT Authentication dan Role-Based Access Control (RBAC).

## Tech Stack

- **Framework**: Django Ninja
- **Authentication**: JWT (django-ninja-jwt)
- **API Extensions**: django-ninja-extra
- **Database**: PostgreSQL
- **Documentation**: Swagger UI (NinjaExtraAPI)

## API Endpoints

### Authentication (`/api/auth/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login and get JWT tokens | No |
| POST | `/api/auth/refresh` | Refresh access token | No |
| GET | `/api/auth/me` | Get current user profile | Yes |
| PUT | `/api/auth/me` | Update current user profile | Yes |

### Courses (`/api/courses/`)

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/courses` | List all courses (public) | No | - |
| GET | `/api/courses/{id}` | Course detail (public) | No | - |
| POST | `/api/courses` | Create new course | Yes | Instructor |
| PATCH | `/api/courses/{id}` | Update course | Yes | Owner |
| DELETE | `/api/courses/{id}` | Delete course | Yes | Admin |

### Enrollments (`/api/enrollments/`)

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| POST | `/api/enrollments` | Enroll to course | Yes | Student |
| GET | `/api/enrollments/my-courses` | My enrolled courses | Yes | - |
| POST | `/api/enrollments/{id}/progress` | Mark lesson complete | Yes | Student |

## Role-Based Access Control (RBAC)

### Available Roles

- **admin**: Full access to all resources
- **instructor**: Can create and manage own courses
- **student**: Can enroll to courses and track progress

### RBAC Decorators

| Decorator | Description |
|-----------|-------------|
| `@is_admin` | Access restricted to admin role only |
| `@is_instructor` | Access restricted to instructor role only |
| `@is_student` | Access restricted to student role only |
| `@is_course_owner` | Access restricted to course owner only |

## JWT Configuration

| Setting | Value |
|---------|-------|
| Access Token Lifetime | 60 minutes |
| Refresh Token Lifetime | 1 day |
| Rotate Refresh Tokens | Yes |
| Blacklist After Rotation | Yes |

## Quick Start

### 1. Start Docker Services

```bash
docker-compose up -d
```

### 2. Run Migrations

```bash
docker exec django_app python /app/code/manage.py migrate
```

### 3. Create Admin User (Optional)

```bash
docker exec -it django_app python /app/code/manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
```

### 4. Access API Documentation

- Swagger UI: http://localhost:8000/api/docs

## API Documentation

### Swagger UI

Interactive API documentation tersedia di `http://localhost:8000/api/docs`

### Postman Collection

Import file `postman_collection.json` ke Postman untuk pengujian API.

## Environment Variables

```
DEBUG=True
DB_NAME=simple_lms
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your-secret-key
```

## Files Structure

```
code/
├── core/
│   ├── apiv1.py      # API endpoints
│   ├── auth.py       # RBAC decorators
│   └── schemas.py    # Pydantic schemas
├── courses/
│   ├── models.py     # Course, Enrollment, UserProgress models
│   └── ...
└── lms/
    ├── settings.py   # Django & Ninja JWT settings
    └── urls.py       # URL routing
```

## Example Usage

### Register User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "email": "student1@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "student"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "password123"
  }'
```

### Create Course (Instructor)

```bash
curl -X POST http://localhost:8000/api/courses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "title": "Python Basics",
    "description": "Learn Python from scratch",
    "category": "programming",
    "level": "beginner"
  }'
```

### Enroll to Course (Student)

```bash
curl -X POST http://localhost:8000/api/enrollments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"course_id": 1}'
```

## Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker logs -f django_app

# Stop services
docker-compose down

# Rebuild and start
docker-compose down && docker-compose build && docker-compose up -d
```
