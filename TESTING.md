# TESTING.md

Comprehensive testing guide for Task Tracker API with all test scenarios.

## Prerequisites

Ensure you have:
1. Python 3.10+ installed
2. Virtual environment activated
3. Dependencies installed: `pip install -r requirements.txt`

## Quick Test Commands

### Run All Tests
```bash
pytest
```

### Run Tests with Verbose Output
```bash
pytest -v
```

### Run Tests with Coverage Report
```bash
pip install pytest-cov
pytest --cov=app --cov-report=html tests/
# Open htmlcov/index.html in browser
```

### Run Specific Test File
```bash
pytest tests/test_health.py
pytest tests/test_tasks.py
```

### Run Specific Test
```bash
pytest tests/test_tasks.py::test_create_task -v
pytest tests/test_tasks.py::test_invalid_transition_done_to_in_progress -v
```

## Test Categories

### 1. Health Check Tests (`test_health.py`)

Verifies API is running and responding correctly.

```bash
pytest tests/test_health.py -v
```

**Tests:**
- `test_health_check` - Confirms health endpoint returns 200 with correct response format

---

### 2. Task CRUD Tests (`test_tasks.py`)

#### Create Task
```bash
pytest tests/test_tasks.py::test_create_task -v
pytest tests/test_tasks.py::test_create_task -v --tb=short
```

**What it tests:**
- Task creation with title and description
- Default status is `todo`
- Task ID is assigned and returned

#### List Tasks
```bash
pytest tests/test_tasks.py::test_list_tasks_empty -v
pytest tests/test_tasks.py::test_list_tasks_with_data -v
```

**What it tests:**
- Empty list when no tasks exist
- Multiple tasks returned correctly

#### Get Task by ID
```bash
pytest tests/test_tasks.py::test_get_task -v
pytest tests/test_tasks.py::test_get_task_not_found -v
```

**What it tests:**
- Retrieving existing task by ID
- 404 error for non-existent task

#### Delete Task
```bash
pytest tests/test_tasks.py::test_delete_task -v
pytest tests/test_tasks.py::test_delete_non_existent_task -v
```

**What it tests:**
- Task deletion
- 404 error when deleting non-existent task

---

### 3. Status Transition Tests (Most Important for ADR-0001)

These tests validate the status workflow per ADR-0001.

#### Valid Transitions

```bash
# Test: todo -> in_progress
pytest tests/test_tasks.py::test_valid_transition_todo_to_in_progress -v

# Test: in_progress -> done
pytest tests/test_tasks.py::test_valid_transition_in_progress_to_done -v
```

**What it tests:**
- `todo` can transition to `todo` or `in_progress`
- `in_progress` can transition to `in_progress` or `done`
- `done` can stay as `done`
- Response is 200 OK with updated status

#### Invalid Transitions (Should Return 422)

```bash
# Test: done -> in_progress (NOT allowed)
pytest tests/test_tasks.py::test_invalid_transition_done_to_in_progress -v

# Test: done -> todo (NOT allowed)
pytest tests/test_tasks.py::test_invalid_transition_done_to_todo -v

# Test: in_progress -> todo (NOT allowed)
pytest tests/test_tasks.py::test_invalid_transition_in_progress_to_todo -v
```

**What it tests:**
- Invalid backward transitions return HTTP 422
- Error message explains the invalid transition
- Task in database remains unchanged

#### Partial Updates

```bash
# Test: Update title without changing status
pytest tests/test_tasks.py::test_update_preserves_status_when_omitted -v

# Test: Update title and description
pytest tests/test_tasks.py::test_update_title_and_description -v
```

**What it tests:**
- Omitting status in update preserves existing status
- Fields can be updated independently
- Only provided fields are modified

---

## Manual Integration Testing

### Start the API Server

```bash
uvicorn app.main:app --reload
```

Server runs at: `http://localhost:8000`
Docs available at: `http://localhost:8000/docs`

### Test Health Endpoint

```bash
curl http://localhost:8000/api/v1/health
```

**Expected Response:**
```json
{
  \"status\": \"healthy\",
  \"message\": \"Task Tracker API is running\"
}
```

### Test Create Task

```bash
curl -X POST http://localhost:8000/api/v1/tasks/ \\
  -H \"Content-Type: application/json\" \\
  -d '{\"title\": \"Buy groceries\", \"description\": \"Milk, eggs, bread\"}'
```

**Expected Response:**
```json
{
  \"id\": 1,
  \"title\": \"Buy groceries\",
  \"description\": \"Milk, eggs, bread\",
  \"status\": \"todo\",
  \"created_at\": \"2026-07-25T19:50:20.123456\",
  \"updated_at\": \"2026-07-25T19:50:20.123456\"
}
```

### Test List Tasks

```bash
curl http://localhost:8000/api/v1/tasks/
```

### Test Get Specific Task

```bash
curl http://localhost:8000/api/v1/tasks/1
```

### Test Valid Status Transition (todo -> in_progress)

```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/1 \\
  -H \"Content-Type: application/json\" \\
  -d '{\"status\": \"in_progress\"}'
```

**Expected Response:**
```json
{
  \"id\": 1,
  \"title\": \"Buy groceries\",
  \"description\": \"Milk, eggs, bread\",
  \"status\": \"in_progress\",
  \"created_at\": \"2026-07-25T19:50:20.123456\",
  \"updated_at\": \"2026-07-25T19:50:21.654321\"
}
```

### Test Invalid Status Transition (in_progress -> todo) - Should Fail

```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/1 \\
  -H \"Content-Type: application/json\" \\
  -d '{\"status\": \"todo\"}'
```

**Expected Response (422 Error):**
```json
{
  \"detail\": \"Invalid transition from 'in_progress' to 'todo'. Allowed transitions: in_progress, done\"
}
```

### Test Update Without Changing Status

```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/1 \\
  -H \"Content-Type: application/json\" \\
  -d '{\"title\": \"Buy groceries and cook dinner\"}'
```

**Expected Response:**
Title updated, status remains `in_progress`

### Test Delete Task

```bash
curl -X DELETE http://localhost:8000/api/v1/tasks/1
```

**Expected Response:**
```json
{
  \"message\": \"Task deleted successfully\"
}
```

---

## Frontend Testing

### 1. Start the Backend

```bash
uvicorn app.main:app --reload
```

### 2. Start the Frontend (in another terminal)

```bash
cd frontend
python -m http.server 5173
```

### 3. Open Browser

Visit: `http://localhost:5173`

### 4. Test Scenarios

**Create a task:**
- Enter title: \"Test task\"
- Enter description: \"This is a test\"
- Click \"Create Task\"
- Verify task appears in the list with \"To Do\" status

**Change status (valid):**
- Click the status dropdown for the task
- Select \"In Progress\"
- Verify status changes to \"In Progress\"

**Try invalid transition:**
- Move task to \"Done\" status
- Try to click status dropdown
- Dropdown should be disabled (no transitions allowed from Done except to Done)

**Update task:**
- If task is not in \"Done\", you can update the title
- Edit the task title and description
- Verify changes are saved

**Delete task:**
- Click \"Delete\" button
- Confirm deletion
- Verify task is removed from list

---

## Test Coverage Report

Generate and view coverage:

```bash
pytest --cov=app --cov-report=html tests/
```

Then open `htmlcov/index.html` to see which lines are covered.

**Coverage Target:**
- Minimum 90% coverage on core business logic
- 100% coverage on status transition validation (critical)

---

## Running All Tests at Once

```bash
# Run all tests, show coverage, generate HTML report
pytest -v --cov=app --cov-report=html --cov-report=term-missing tests/
```

**Output will show:**
- Total tests run
- Pass/fail count
- Coverage percentage
- Missing lines in coverage

---

## Test Structure Overview

```
tests/
├── conftest.py                 # Pytest fixtures (session, client)
├── test_health.py              # 1 test
└── test_tasks.py               # 14 tests
    ├── CRUD Tests (5)
    │   ├── test_create_task
    │   ├── test_list_tasks_empty
    │   ├── test_list_tasks_with_data
    │   ├── test_get_task
    │   └── test_delete_task
    ├── Transition Validation Tests (6)
    │   ├── test_valid_transition_todo_to_in_progress
    │   ├── test_valid_transition_in_progress_to_done
    │   ├── test_invalid_transition_done_to_in_progress
    │   ├── test_invalid_transition_done_to_todo
    │   ├── test_invalid_transition_in_progress_to_todo
    │   └── test_update_preserves_status_when_omitted
    └── Error Handling Tests (3)
        ├── test_get_task_not_found
        ├── test_delete_non_existent_task
        └── test_update_title_and_description
```

**Total: 15 tests**

---

## Troubleshooting

### Tests fail with \"ModuleNotFoundError\"

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate      # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Database lock error

```bash
# Remove any stale database files
rm task_tracker.db
rm -rf __pycache__ .pytest_cache

# Run tests again
pytest
```

### Port 8000 already in use

```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

### Frontend can't connect to API

- Confirm backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Verify CORS is enabled in `app/main.py`

---

## Success Criteria

All tests pass when:

✅ `pytest` runs with 15/15 tests passing
✅ Coverage >= 90%
✅ All status transitions work as defined in ADR-0001
✅ Invalid transitions return HTTP 422
✅ Frontend loads and connects to API
✅ Tasks persist in SQLite database
✅ No authentication errors (not implemented)
✅ Database is created automatically on startup

---

## Key Testing Principles (Based on FastAPI Best Practices)

### 1. Request Body and Response Models
- **TaskCreate** is the request body schema (POST endpoint)
- **TaskUpdate** is the request body schema (PATCH endpoint)
- **TaskRead** is the response model (all GET, POST, PATCH endpoints)
- Status codes are defined on route decorators

### 2. Path vs Query Parameters
- Path parameters: `/tasks/{task_id}` - required, part of URL
- Query parameters: not used in basic CRUD (but could add `?status=todo` for filtering)
- Return 200 with empty list when no matches found
- Return 404 when specific resource not found

### 3. Error Handling
- Raise `HTTPException` for business logic failures (e.g., invalid status transitions)
- Pydantic validates field constraints automatically (title length, enum values)
- State transition validation happens in service layer before database commit

### 4. Pydantic v2 Models
- All request/response models use Pydantic BaseModel
- Enums for status values (TaskStatus enum in both schemas and models)
- `from_attributes = True` in TaskRead to support SQLModel instances
- Optional fields default to None (not required in PATCH)

### 5. PATCH and Partial Updates
- Only provided fields are updated (exclude_unset behavior)
- Validation happens BEFORE any database changes
- Invalid state transitions return 422 without modifying task

### 6. Testing with pytest and Fixtures
- `conftest.py` provides isolated in-memory SQLite per test
- `client` fixture uses TestClient for endpoint testing
- `session` fixture provides database session for tests
- Each test is independent and doesn't affect production database
- Status code assertions: 200 (success), 404 (not found), 422 (validation error), 200 with empty list

---

## Next Steps

Once all tests pass:

1. Review test coverage with `pytest --cov=app --cov-report=html`
2. Verify API documentation at `http://localhost:8000/docs`
3. Test frontend at `http://localhost:5173`
4. Try the example curl commands above
5. Consider adding more features (pagination, filtering, etc.)
",
  "message": "Add comprehensive testing guide with all test scenarios",
  "owner": "FawziSandikly",
  "path": "TESTING.md",
  "repo": "task-tracker-api"
}
