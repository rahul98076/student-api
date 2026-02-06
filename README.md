# Student API

A production-grade REST API for managing student records, built with Python (Flask), SQLite, and Docker-ready architecture. This project implements the Twelve-Factor App methodology.

## Features

- CRUD Operations: Create, Read, Update, Delete students
- Database: SQLite with Flask-Migrate for schema management
- Best Practices: API Versioning (/api/v1), Structured Logging, and Healthchecks
- Containerization: Multi-stage Docker build with non-root user security
- Testing: Automated unit tests with pytest and in-memory databases
- Configuration: Environment-based config using .env

## Tech Stack

- **Language:** Python 3.14
- **Framework:** Flask
- **ORM:** SQLAlchemy
- **Container:** Docker (Multi-stage)
- **Testing:** Pytest
- **Tooling:** Makefile, Postman

## Project Structure

```
student-api/
├── app/                    # Application package
│   ├── __init__.py         # Flask app factory and route definitions
│   ├── extensions.py       # SQLAlchemy and Migrate extensions
│   ├── models.py           # Database models (Student)
│   └── __pycache__/
├── instance/               # Instance-specific files (generated)
├── migrations/             # Alembic database migrations
│   ├── versions/           # Migration scripts
│   ├── alembic.ini         # Alembic configuration
│   └── env.py              # Alembic environment setup
├── tests/                  # Test suite
│   ├── conftest.py         # Pytest fixtures and configuration
│   ├── test_students.py    # Student API tests
│   └── __pycache__/
├── run.py                  # Application entry point
├── Makefile                # Common commands
├── requirements.txt        # Python dependencies
├── readme.md               # This file
└── Student API.postman_collection.json  # Postman collection for API testing
```

## Local Setup (Non-Docker)

1. Prerequisites
   - Python 3.x installed.
   - make (optional, for using the Makefile shortcuts).

2. Installation
   Clone the repository and install dependencies using the Makefile:
   ```bash
   make setup
   make install
   ```
   Alternatively, create a venv manually and run:
   ```bash
   pip install -r requirements.txt
   ```

3. Configuration
   Create a `.env` file in the root directory:
   ```
   FLASK_APP=run.py
   FLASK_DEBUG=1
   DATABASE_URL=sqlite:///students.db
   ```

4. Database Setup
   Initialize the SQLite database and apply migrations:
   ```bash
   flask db upgrade
   ```

## Running the Application (Local)

Start the server:
```bash
make run
```
The API will be available at http://127.0.0.1:5000

## Docker Support

This application is containerized using a Multi-Stage Dockerfile for optimized image size and security.

1. Build the Image
   Build the Docker image using the Makefile. You can specify a version tag (default is v1).
   Build version v1.0.0
   ```bash
   make docker-build VERSION=v1.0.0
   ```

2. Run the Container
   Run the container locally. This command injects your local .env variables into the container and maps port 5000.
   Run version v1.0.0
   ```bash
   make docker-run VERSION=v1.0.0
   ```
   The API will be available at http://localhost:5000.

3. Manual Docker Commands
   If you prefer not to use Make:

   Build
   ```bash
   docker build -t student-api:v1.0.0 .
   ```

   Run (Injecting env vars and mapping ports)
   ```bash
   docker run --rm -p 5000:5000 --env-file .env student-api:v1.0.0
   ```

## API Endpoints

Method | Endpoint | Description
---|---:|---
GET | /healthcheck | Service health status
GET | /api/v1/students | Get all students
POST | /api/v1/students | Create a new student
GET | /api/v1/students/<id> | Get specific student
PUT | /api/v1/students/<id> | Update student details
DELETE | /api/v1/students/<id> | Delete a student

### Example: Create a student
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

Run the automated test suite:
```bash
make test
```
Tests are located in the `tests/` directory using pytest. The suite uses in-memory databases for fast, isolated runs.

## Logging

The application includes structured logging at INFO level; logs include endpoint calls and CRUD operations.

## Student Model

The Student model includes the following fields:
- `id` (Integer, Primary Key) - Auto-generated student ID
- `first_name` (String, Required) - Student's first name
- `last_name` (String, Required) - Student's last name
- `grade` (String, Required) - Current grade level
- `email` (String, Required, Unique) - Student's email address

## License

This project is part of the One2N SRE bootcamp curriculum.
