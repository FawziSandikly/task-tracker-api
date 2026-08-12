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
- ✅ Due Dates support
- ✅ Overdue task filtering
- ✅ Task Tags for organization
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
- **GET** `/api/v1/tasks/?filter=overdue` - List overdue tasks
- **GET** `/api/v1/tasks/?tag=work` - Filter tasks by tag
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
├── .github/workflows/
│   └── ci.yml                  # GitHub Actions CI pipeline
├── Dockerfile                  # Docker configuration
├── .dockerignore                # Docker build exclusions
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
  due_date DATETIME NULL,
  tags TEXT,
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
- ✅ CRUD operations
- ✅ Status transition validation
- ✅ Due date validation
- ✅ Overdue task filtering
- ✅ Tag creation and updates
- ✅ Invalid requests and edge cases
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

## Final Project

**Branch reviewed**: final-project

### What this submission demonstrates

- ✅ **Existing Task Tracker app still runs** inside the intended course scope
- ✅ **CI runs the pytest suite** on push and pull request to main/final-project
- ✅ **Docker image builds and runs** with /health returning HTTP 200
- ✅ **AI review, security, and ownership evidence** in docs/ folder
- ✅ **No new product features added** - only release infrastructure and documentation
- ✅ **No changes to app/ or frontend/** except documented guardrails

### How to run locally

```bash
# Clone and setup
git clone https://github.com/FawziSandikly/task-tracker-api.git
cd task-tracker-api
git checkout final-project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, verify health check
curl http://localhost:8000/api/v1/health
# Expected: {"status": "ok"}
```

### How to run tests

```bash
# Full test suite
pytest

# With coverage
pytest --cov=app tests/

# Specific test file
pytest tests/test_health.py
```

### How to run with Docker

```bash
# Build the image
docker build -t task-tracker:latest .

# Run the container
docker run -p 8000:8000 task-tracker:latest

# Verify health endpoint (in another terminal)
curl http://localhost:8000/api/v1/health
# Expected: {"status": "ok"} - HTTP 200
```

### Evidence files

- **docs/release-evidence.md** - Baseline app/tests, CI workflow, Docker build/run, documentation verification
- **docs/final-ai-review.md** - AI code review mini-log, security findings, ownership statement
- **docs/ai-playbook.md** - Personal AI usage rules, decision card, and course evidence
- **AGENTS.md** - Project guardrails, tech stack, run/test commands, AI integration guidelines

### AI assistance summary

**AI helped draft or review**: Infrastructure (Dockerfile, CI/CD), Documentation (README, evidence), Release checklist

**Verified by**: Local testing (app runs, /health returns 200), Docker build and run, pytest execution, diff review of all generated files

**One AI suggestion I rejected**: AI suggested using `continue-on-error: true` in CI workflow to allow tests to pass even if they fail. This violates the course rule against dangerous shortcuts. I removed this and ensured the workflow fails fast on test failure—the correct behavior.

## Next Steps

Future improvements include:
- User authentication
- Pagination
- Search functionality
- Task priorities
- Task comments
- Notifications
- Alembic database migrations
- Deployment using PostgreSQL and Docker

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangelo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## License

This project is for learning purposes.
