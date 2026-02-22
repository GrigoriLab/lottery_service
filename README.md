# Lottery Service

A Django REST API for running lotteries. Participants register, submit ballots for active lotteries, and winners are selected randomly via a celery periodic task.

## Prerequisites

- python 3.13
- poetry
- docker & docker compose

## Environment Files

The project uses two separate environment files:

- **`.env`** — for local development. Points to `localhost` with exposed Docker ports (e.g. `localhost:5438` for Postgres, `localhost:6380` for Redis). Used when running the Django server locally (via PyCharm, `manage.py runserver`, etc.) while only DB and Redis run in Docker.
- **`.env.docker`** — for running everything inside Docker. Uses internal Docker hostnames and ports (e.g. `db:5432`, `redis:6379`). Used with `docker compose --env-file .env.docker up`.

Create both from the provided examples:

```bash
cp .env.example .env
cp .env.docker.example .env.docker
```

## Quick Start (Docker)

1. Start all services:

```bash
docker compose --env-file .env.docker up --build
```

This starts PostgreSQL, Redis, the lottery service, celery worker, and celery beat.

2. Run migrations:

```bash
make migrate
```

3. Create a superuser for Django admin:

```bash
make createsuperuser
```

4. Set up periodic tasks:

```bash
make setup_periodic_tasks
```

5. Load test data:

```bash
make load_test_data
```

The service is available at http://localhost:8000. Django admin is at http://localhost:8000/admin/.

## Local Development

For local development, only DB and Redis run in Docker while you run the Django server directly (e.g. via PyCharm or terminal). This uses `.env` with `localhost` addresses.

1. Start database and Redis:

```bash
make db_and_redis
```

2. Install dependencies and run migrations:

```bash
poetry install --no-root
poetry run python manage.py migrate
```

3. Run the development server:

```bash
poetry run python manage.py runserver
```

## API Documentation

Interactive API documentation is available at:

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## API Usage

All API endpoints are prefixed with `/api/v1/`.

### Register a participant

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "password123"}'
```

### Obtain JWT token

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "password123"}'
```

Save the `access` token from the response for authenticated requests.

### List lotteries

```bash
curl http://localhost:8000/api/v1/lotteries/
```

### Create lottery

Lotteries are created through the Django admin panel at http://localhost:8000/admin/.

### Submit a ballot

Requires authentication. Submit a ballot for an active lottery:

```bash
curl -X POST http://localhost:8000/api/v1/ballots/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"lottery": 1}'
```

### Check winners

Requires authentication. Optionally filter by date:

```bash
curl http://localhost:8000/api/v1/winners/ \
  -H "Authorization: Bearer <access_token>"

curl "http://localhost:8000/api/v1/winners/?date=2026-02-22" \
  -H "Authorization: Bearer <access_token>"
```
