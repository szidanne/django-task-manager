# Task Manager Django

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](#)
[![Django](https://img.shields.io/badge/Django-5.x-0C4B33?logo=django&logoColor=white)](#)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.x-A30000?logo=django&logoColor=white)](#)
[![TailwindCSS](https://img.shields.io/badge/Tailwind%20CSS-3.x-06B6D4?logo=tailwindcss&logoColor=white)](#)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](#)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-Server-499848?logo=gunicorn&logoColor=white)](#)
[![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?logo=nginx&logoColor=white)](#)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](#)
[![JWT](https://img.shields.io/badge/Auth-JWT-black?logo=jsonwebtokens&logoColor=white)](#)
[![Swagger](https://img.shields.io/badge/OpenAPI-Swagger-85EA2D?logo=swagger&logoColor=black)](#)
[![Postman](https://img.shields.io/badge/Tested%20with-Postman-FF6C37?logo=postman&logoColor=white)](#)

---

## Project Overview

A Django web app with a `Tailwind / DaisyUI` UI, containerized via `Docker`. `Nginx` serves static files; `PostgreSQL` DB; `DRF` provides APIs with `Swagger/Redoc` docs.

---

## Features

- User authentication and account management
- Non-responsive UI powered by Tailwind CSS & DaisyUI
- PostgreSQL database
- Dockerized setup with isolated services for web, db, and nginx
- OpenAPI docs (Swagger UI + ReDoc)

---

## Tech Stack
- **Backend:** Django, Django REST Framework, Gunicorn  
- **Frontend:** TailwindCSS (CLI or `django-tailwind`)  
- **DB:** PostgreSQL  
- **Proxy/Static:** Nginx  
- **Containerization:** Docker & Docker Compose  
- **Docs:** drf-yasg (Swagger/Redoc)

---

## Project Structure

```
├── manage.py
├── theme/
│ ├── static_src/ # Tailwind input/config (e.g., src/input.css)
│ ├── static/ # App static (pre-collectstatic), e.g., css/dist/styles.css
├── staticfiles/ # STATIC_ROOT output (post collectstatic, served by Nginx)
├── nginx/
│ └── nginx.conf
├── docker-compose.yml
├── requirements.txt
└── README.md 
```
---

# Setup & Installation

## Prerequisites
- Docker & Docker Compose
- (Optional for local dev) Node.js + npm if running the Tailwind CLI locally

## Setup
1. Clone repo. 
2. Copy the provided env → `.env.docker` and adjust secrets if needed.
3. Build and run containers: `docker compose up --build`
4. One-time init / every fresh build (execute inside web container)
    ```shell
    # collect static, create/apply migrations
    docker compose exec web python manage.py collectstatic --noinput
    docker compose exec web python manage.py makemigrations
    docker compose exec web python manage.py migrate
    ```
5. Open the app: http://127.0.0.1:8000/
 (if you expose Django directly)
or http://localhost/
 (through Nginx on port 80, if configured that way)

## Running Locally (without Docker)

Follow these steps to set up and run the project locally:

1. Copy the provided env → `.env.local` and adjust secrets if needed.
2. Create & activate virtual environment
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3. Install Python deps
    ```bash
    pip install -r requirements.txt
    ```
4. Install Tailwind deps
    ```bash
    cd theme/static_src
    npm install
    cd ../..
    ```
5. Start Django server with Tailwind watcher
    ```bash
    python manage.py tailwind dev
    ```


---
## API Documentation
1. Swagger UI: http://127.0.0.1:8000/tasks/api/docs/
2. Redoc: http://127.0.0.1:8000/tasks/api/redoc/

## 🔑 Authentication & Testing (JWT)

### Obtain token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"youruser","password":"yourpass"}'
```

**Response example**
```terminaloutput
{ "access": "<ACCESS_TOKEN>", "refresh": "<REFRESH_TOKEN>" }
```

### Use token in any client
(**Swagger** “Authorize” button, **Postman**, mobile app, etc.)
```bash
curl http://127.0.0.1:8000/api/protected-endpoint/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Refresh Token
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<REFRESH_TOKEN>"}'
```

---

## Useful Commands

```bash
# run tests
cd tasks/tests
pytest test_apis.py
pytest test_models.py

# create superuser
python manage.py createsuperuser

# rebuild stack
docker compose down -v
docker compose up --build
```
