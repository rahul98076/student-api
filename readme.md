# Student API

A RESTful API built with Flask for managing student records. This project demonstrates best practices for building a Python-based REST API, including database models, migrations, and comprehensive testing.

## Features

- Create, read, update, and delete student records
- SQLAlchemy ORM for database interactions
- Alembic database migrations
- Pytest test suite
- Comprehensive logging
- Health check endpoint
- Environment-based configuration

## Tech Stack

- **Framework:** Flask
- **Database ORM:** SQLAlchemy
- **Database Migrations:** Flask-Migrate (Alembic)
- **Testing:** pytest
- **Environment Management:** python-dotenv

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

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository and navigate to the project directory:
```bash
cd student-api
```

2. Create and activate a virtual environment:
```bash
make setup
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # macOS/Linux
```

3. Install dependencies:
```bash
make install
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
DATABASE_URL=sqlite:///students.db
FLASK_ENV=development
```

5. Initialize the database:
```bash
flask db upgrade
```

## Running the Application

Start the development server:
```bash
make run
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/healthcheck` - Returns API health status
  ```json
  {"status": "ok"}
  ```

### Students

#### List all students
- **GET** `/api/v1/students`
  - Returns a list of all student records

#### Get a specific student
- **GET** `/api/v1/students/<id>`
  - Returns a single student by ID

#### Create a new student
- **POST** `/api/v1/students`
  - Request body:
    ```json
    {
      "first_name": "John",
      "last_name": "Doe",
      "grade": "10",
      "email": "john@example.com"
    }
    ```
  - Returns the created student record with ID (201 Created)

#### Update a student
- **PUT** `/api/v1/students/<id>`
  - Request body (all fields optional):
    ```json
    {
      "first_name": "Jane",
      "last_name": "Smith",
      "grade": "11",
      "email": "jane@example.com"
    }
    ```
  - Returns the updated student record

#### Delete a student
- **DELETE** `/api/v1/students/<id>`
  - Returns 204 No Content on success

## Testing

Run the test suite:
```bash
make test
```

Tests are located in the `tests/` directory using pytest framework. The test suite includes:
- Fixtures for database setup (conftest.py)
- Student API endpoint tests (test_students.py)

## Database Migrations

The project uses Alembic for database schema management.

View migration history:
```bash
flask db history
```

Create a new migration:
```bash
flask db migrate -m "Description of changes"
```

Apply migrations:
```bash
flask db upgrade
```

## API Testing

A Postman collection is included (`Student API.postman_collection.json`) for easy testing of all endpoints. Import this file into Postman to test the API.

## Logging

The application includes comprehensive logging at the INFO level. Logs are output to the console and include information about:
- API endpoint calls
- Student record creation, updates, and deletions
- Database operations

## Development

For development setup, ensure `FLASK_ENV=development` is set in your `.env` file. This enables debug mode and auto-reloading of the development server.

## Student Model

The Student model includes the following fields:
- `id` (Integer, Primary Key) - Auto-generated student ID
- `first_name` (String, Required) - Student's first name
- `last_name` (String, Required) - Student's last name
- `grade` (String, Required) - Current grade level
- `email` (String, Required, Unique) - Student's email address

## License

This project is part of the SRE bootcamp curriculum.
