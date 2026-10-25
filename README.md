# SupportFlow AI

A RESTful ticket management API built with Python, FastAPI, and SQLite.

This project focuses on backend engineering fundamentals, including API development, data persistence, request validation, error handling, and automated testing.

**Current version:** Backend MVP (v1). AI-powered features are planned for future versions and are not yet implemented.

## Features

- Create support tickets with title, description, and priority
- List all tickets and retrieve individual tickets by ID
- Update ticket status
- Delete tickets
- Persist data using SQLite
- Validate API requests using Pydantic
- Handle HTTP 404 and 422 errors
- Automatically initialize the database on application startup
- Run automated tests using Pytest

## Tech Stack

- **Python** — Backend programming
- **FastAPI** — REST API framework
- **Pydantic** — Request validation
- **SQLite** — Database
- **Pytest** — Automated testing
- **Git & GitHub** — Version control

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/tickets` | List all tickets |
| GET | `/tickets/{id}` | Retrieve a ticket |
| POST | `/tickets` | Create a ticket |
| PATCH | `/tickets/{id}` | Update ticket status |
| DELETE | `/tickets/{id}` | Delete a ticket |

### Example: Create a ticket

**POST `/tickets`**

```json
{
  "title": "Login issue",
  "description": "User cannot access the platform",
  "priority": "high"
}
```

**Example response — HTTP 201**

```json
{
  "id": 1,
  "title": "Login issue",
  "description": "User cannot access the platform",
  "priority": "high",
  "status": "open"
}
```

Supported priorities: `low`, `medium`, `high`, `urgent`.

Supported statuses: `open`, `in_progress`, `resolved`.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/renatocandido0/supportflow_ai.git
cd supportflow_ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the API

```bash
python -m uvicorn main:app --reload
```

The application automatically creates the SQLite database and tickets table if they do not already exist.

### 5. Explore the API

Open the interactive Swagger documentation:

http://127.0.0.1:8000/docs

## Running Tests

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the automated test suite:

```bash
python -m pytest -v
```

The project currently includes eight passing automated tests covering API operations, error handling, ticket formatting, and database initialization.

## Roadmap

Planned improvements include:

- AI-assisted ticket classification and prioritization
- Additional validation and automated test coverage
- PostgreSQL integration
- Docker containerization
- CI/CD pipeline
- Cloud deployment and monitoring

These features are planned and are not part of the current version.

## Project Status

**Version 1 — Functional backend MVP**

This project is being developed incrementally as part of a software engineering and artificial intelligence learning journey.