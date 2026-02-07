# Student API (SRE Bootcamp)

A production-grade REST API for managing student records. The service is implemented with Python (Flask) and is container-first — the repository includes a Docker Compose configuration that provisions a PostgreSQL 15 database with a persistent volume.

## Highlights

- **CRUD Operations:** Create, Read, Update, Delete students.
- **Database:** PostgreSQL 15 (containerized) with a named volume for persistence.
- **Orchestration:** Docker Compose for reproducible local environments.
- **Migrations:** Flask-Migrate (Alembic) used to manage schema changes.
- **Healthchecks:** Services expose healthchecks and the Compose setup waits for dependencies.
- **Testing:** Unit tests with pytest; test tooling available via `make`.

## Tech Stack

- **Language:** Python 3.14
- **Framework:** Flask
- **Database:** PostgreSQL 15
- **Containerization:** Docker & Docker Compose
- **Testing:** Pytest
- **Tooling:** Makefile, Postman

## Quick Start (recommended)

This project is intended to run with Docker Compose. The Compose file starts two services: `db` (Postgres) and `api` (the Flask app). The `api` service is configured with a `DATABASE_URL` that points to the `db` service.

Prerequisites

- Docker
- GNU `make` 

**Automatic Setup (Recommended):**
We have included a script to check for and install these tools automatically.
```bash
make setup
```
Manual Install: If you prefer to install them manually:

[Docker](https://www.docker.com/products/docker-desktop)

[GNU make](https://www.gnu.org/software/make/)

Start the stack and apply migrations:

```bash
make start
```

Notes

- API: http://localhost:5000
- Postgres: localhost:5432 (credentials provided in `docker-compose.yml`: user `postgres`, password `password`, database `student_db`)

Common Make targets

| Command | Description |
| --- | --- |
| `make start` | Start API + DB, wait for healthchecks, and migrate schema |
| `make up` | Start services in detached mode (`docker compose up -d`) |
| `make down` | Stop services (`docker compose down`) |
| `make logs` | Follow logs for all services (`docker compose logs -f`) |
| `make migrate` | Run `flask db upgrade` inside the API container |
| `make clean-docker` | Stop services and remove volumes (`docker compose down -v`) |
| `make test` | Run unit tests locally (`pytest`) |

## Environment / Configuration

The service reads configuration from environment variables. When using Docker Compose the `api` service is given a `DATABASE_URL` that points at the `db` service. When running locally (non-container) update your `.env` accordingly.

Example `.env` for local Postgres (replace values as needed):

```dotenv
FLASK_APP=run.py
FLASK_DEBUG=1
FLASK_SECRET_KEY=change-me
DATABASE_URL=postgresql://postgres:password@localhost:5432/student_db
```

Note: the repository currently contains a `.env` with a SQLite `DATABASE_URL` value for quick local runs; update it if you prefer Postgres locally.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/healthcheck` | Service health status |
| GET | `/api/v1/students` | Get all students |
| POST | `/api/v1/students` | Create a new student |
| GET | `/api/v1/students/<id>` | Get specific student |
| PUT | `/api/v1/students/<id>` | Update student details |
| DELETE | `/api/v1/students/<id>` | Delete a student |

## Local (non-Docker) setup

If you want to run the application without containers:

1. Create a virtual environment and install dependencies:

```bash
make setup
source .venv/bin/activate  # on Windows: .venv/Scripts/activate
pip install -r requirements.txt
```

2. Configure `.env` to point to your Postgres instance (see example above).

3. Run migrations and start the app:

```bash
flask db upgrade
python run.py
```

## Example: Create a student

Request body:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "grade": "10",
  "email": "john@example.com"
}
```

## Testing

Run tests locally via Make:

```bash
make test
```

## Logging

The application uses structured logging (INFO level) and logs include endpoint calls and CRUD operations.

## Student Model

The `Student` model includes these fields:

- `id` (Integer, Primary Key)
- `first_name` (String, required)
- `last_name` (String, required)
- `grade` (String, required)
- `email` (String, required, unique)

## Notes

- The Compose file in this repository provisions Postgres 15 and a named volume `postgres_data` for persistence.
- The Makefile exposes convenient shortcuts (`make start`, `make migrate`, `make logs`, etc.).

---

This README was synchronized with the repository's Docker Compose and Makefile settings.