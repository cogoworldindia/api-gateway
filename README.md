# API Gateway

## Prerequisites
- Python 3.11+
- Poetry or pip virtual environment
- Running downstream services:
  - Auth service at `http://127.0.0.1:8083`
  - User service at `http://127.0.0.1:8081`
  - Email service at its configured URL

## Configuration
1. Copy `.env.example` to `.env` (create one if missing).
2. Set required variables:
   ```
   APP_PORT=8000
   AUTH_SERVICE_URL=http://127.0.0.1:8083
   USER_SERVICE_URL=http://127.0.0.1:8081
   EMAIL_SERVICE_URL=http://127.0.0.1:8082
   JWT_SECRET_KEY=<jwt-secret>
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   REDIS_URL=redis://localhost:6379/0
   ```
   Adjust URLs and credentials for your environment.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port ${APP_PORT:-8000}
```

## Routing
- Gateway exposes routes under `/v1/api`.
- Requests are proxied to the corresponding downstream services:
  - `/v1/api/auth/**` → Auth service
  - `/v1/api/users/**` → User service (requires `Authorization` header; validated via auth service)
  - `/v1/api/emails/**` → Email service

## Health Check
`GET /health` returns the gateway status in the standard response format.
