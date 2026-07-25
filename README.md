# Task Tracker REST API

A learning-focused task tracker REST API built with FastAPI, SQLModel, and SQLite.

## Architecture

This project implements the decisions from ADR-0001:
- **Framework**: FastAPI with Python 3.12
- **Database**: SQLite with SQLModel ORM
- **Validation**: Pydantic for request/response schemas
- **Testing**: pytest with isolated SQLite databases

## Features

- ✅ CRUD operations for tasks
- ✅ Status workflow: `todo` → `in_progress` → `done`
- ✅ Status transition validation (backward transitions rejected)
- ✅ Partial updates preserve omitted fields
- ✅ Health check endpoint
- ✅ Comprehensive test coverage
- ✅ CORS enabled for local frontend integration

## Quick Start

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/FawziSandikly/task-tracker-api.git
cd task-tracker-api
```

2. **Create a virtual environment**
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the API

```bash
# Start development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Running Tests

```bash
# Run all tests with verbose output
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/test_health.py
```

## API Endpoints

### Health Check
- **GET** `/api/v1/health` - Check API status

### Tasks
- **POST** `/api/v1/tasks/` - Create a new task
- **GET** `/api/v1/tasks/` - List all tasks
- **GET** `/api/v1/tasks/{id}` - Get task by ID
- **PATCH** `/api/v1/tasks/{id}` - Update task
- **DELETE** `/api/v1/tasks/{id}` - Delete task

## Status Transitions

Valid transitions per ADR-0001:
- `todo` → `todo` (no change) ✅
- `todo` → `in_progress` ✅
- `in_progress` → `in_progress` (no change) ✅
- `in_progress` → `done` ✅
- `done` → `done` (no change) ✅

Invalid transitions return HTTP 422:
- `done` → `in_progress` ❌
- `done` → `todo` ❌
- `in_progress` → `todo` ❌

## Example Usage

### Create a task
```bash
curl -X POST http://localhost:8000/api/v1/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk and eggs"}'
```

### List all tasks
```bash
curl http://localhost:8000/api/v1/tasks/
```

### Update task status
```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

### Invalid status transition
```bash
# This returns 422 error - can't go from done back to in_progress
curl -X PATCH http://localhost:8000/api/v1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

## Project Structure

```
task-tracker-api/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   └── config.py           # Settings and environment variables
│   ├── db/
│   │   └── session.py          # Database engine and session management
│   ├── models/
│   │   └── task.py             # SQLModel database models
│   ├── schemas/
│   │   └── task.py             # Pydantic request/response schemas
│   ├── services/
│   │   └── task_service.py     # Business logic and validation
│   └── api/v1/
│       └── endpoints/
│           ├── health.py       # Health check endpoint
│           └── tasks.py        # Task CRUD endpoints
├── tests/
│   ├── test_health.py          # Health endpoint tests
│   └── test_tasks.py           # Task business logic tests
├── frontend/                   # Separate frontend application
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── pytest.ini                  # pytest configuration
├── conftest.py                 # pytest fixtures
└── README.md                   # This file
```

## Database

Tasks are stored in SQLite at `./task_tracker.db`. The database is created automatically on first run.

### Schema
```sql
CREATE TABLE tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title VARCHAR NOT NULL,
  description VARCHAR DEFAULT '',
  status VARCHAR DEFAULT 'todo',
  created_at DATETIME DEFAULT NOW(),
  updated_at DATETIME DEFAULT NOW()
);
```

## Testing Strategy

Each test:
1. Uses an isolated in-memory SQLite database
2. Does not affect the main `task_tracker.db` file
3. Is fully independent from other tests
4. Tests both valid operations and error cases

### Test Coverage
- ✅ Health check endpoint
- ✅ Task creation with default status
- ✅ Task listing (empty and with data)
- ✅ Task retrieval by ID (found and 404 cases)
- ✅ Valid status transitions
- ✅ Invalid status transitions (422 responses)
- ✅ Partial updates (omitted fields preserved)
- ✅ Task deletion

## Development

### Adding a new feature
1. Add model to `app/models/`
2. Add schema to `app/schemas/`
3. Add service logic to `app/services/`
4. Add endpoint to `app/api/v1/endpoints/`
5. Add tests to `tests/`

### Local frontend integration
Run the frontend on a different port:
```bash
cd frontend
python -m http.server 5173
```

The backend CORS configuration allows requests from any origin during development.

## Next Steps

Once comfortable with this setup, consider:
- Adding pagination to task listing
- Implementing filtering by status
- Adding task categories/projects
- Adding due dates
- Implementing task comments
- Adding user authentication
- Using Alembic for schema migrations
- Deploying with production database

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## License

This project is for learning purposes.