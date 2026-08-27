# AGENTS.md - AI Assistant Guidelines for Task Tracker

This document establishes guardrails for AI-assisted work on the Task Tracker API project.

## Project Overview

**Repository**: FawziSandikly/task-tracker-api  
**Branch**: final-project  
**Tech Stack**:
- Backend: Python 3.12, FastAPI, SQLModel, SQLite
- Testing: pytest with isolated in-memory databases
- Container: Docker with non-root user
- CI/CD: GitHub Actions

## How to Run the Project

### Local Setup
```bash
# Clone the repository
git clone https://github.com/FawziSandikly/task-tracker-api.git
cd task-tracker-api

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests
```bash
# Run full test suite
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_health.py
```

### Health Check
```bash
curl http://localhost:8000/api/v1/health
# Expected response: {"status": "ok"}
```

### Running with Docker
```bash
# Build image
docker build -t task-tracker:latest .

# Run container
docker run -p 8000:8000 task-tracker:latest

# Test health endpoint
curl http://localhost:8000/api/v1/health
```

## Project Rules (Non-Negotiable)

1. **No new product features**: Do not add comments, authentication, notifications, or unrelated UI changes
2. **Protect app/ and frontend/**: Only modify for bug fixes, security fixes, or documented corrections
3. **No secrets or personal data**: Never paste credentials, .env values, tokens, or real data into AI tools
4. **Scope stays inside course deliverables**: This is a learning project, not production code
5. **Test coverage required**: Any changes must maintain or improve test passing rate
6. **Documentation must be accurate**: README and docs must reflect actual behavior

## AI Guardrails

### Docs-First / Read-First
- Before asking AI to write code, read the existing code structure (app/main.py, app/services/, tests/)
- Check README.md, ADR-0001, and existing comments for context
- Share relevant file paths with AI to ground responses in actual project structure

### When to Use AI
✅ **Appropriate uses**:
- Scaffolding CI/CD pipelines (.github/workflows/ci.yml, Dockerfile)
- Generating documentation (README updates, docstrings)
- Writing test cases (pytest structure, fixtures)
- Debugging common issues (error messages, stack traces)
- Code review and security analysis

❌ **Inappropriate uses**:
- Rewriting core business logic without understanding current behavior
- Generating code without reviewing it line-by-line
- Accepting AI suggestions without testing
- Pasting production logs or real user data
- Using AI to bypass understanding of the codebase

### Code Review Process
1. **Request**: Ask AI to review a specific file or diff, not the entire repo
2. **Grade**: Classify each AI comment as Useful, Noise, or Wrong
3. **Verify**: Run tests or manually check the suggestion before accepting
4. **Document**: Record the AI comment, your grade, and your decision in docs/final-ai-review.md

### Security Checklist (Always Manual)
- [ ] No secrets in .env file committed to repo
- [ ] No database passwords hardcoded
- [ ] Non-root user in Dockerfile
- [ ] Health check endpoint doesn't expose sensitive data
- [ ] CORS settings appropriate for local development only
- [ ] No dangerous shortcuts in CI (continue-on-error: true, || true, skipped tests)

## File Structure

```
task-tracker-api/
├── app/
│   ├── main.py                 # FastAPI entry point (do not modify without reason)
│   ├── core/
│   │   └── config.py           # Settings
│   ├── db/
│   │   └── session.py          # Database setup
│   ├── models/
│   │   └── task.py             # SQLModel Task model
│   ├── schemas/
│   │   └── task.py             # Pydantic schemas
│   ├── services/
│   │   └── task_service.py     # Business logic
│   └── api/v1/endpoints/
│       ├── health.py           # Health check
│       └── tasks.py            # Task CRUD endpoints
├── tests/
│   ├── test_health.py          # Health endpoint tests
│   └── test_tasks.py           # Task CRUD tests
├── frontend/                   # Separate frontend app (do not modify)
├── Dockerfile                  # Docker configuration
├── .dockerignore                # Docker build exclusions
├── .github/workflows/ci.yml    # CI/CD pipeline
├── conftest.py                 # pytest fixtures
├── pytest.ini                  # pytest configuration
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Integration Points for AI Review

### When reviewing AI output, ask:
1. **Accuracy**: Does this match the actual codebase? Can I run it?
2. **Safety**: Does it introduce secrets, hardcoding, or unsafe shortcuts?
3. **Scope**: Does it stay within the course rules (no new features)?
4. **Testing**: Will it pass pytest? Have I verified with `pytest`?
5. **Documentation**: Is it reflected in README or docs/?

## Escalation

If AI suggests something that violates these rules:
1. Document the suggestion in docs/final-ai-review.md with your grade
2. Explain why it was rejected (violates project rules, introduces risk, fails tests)
3. Describe what you did instead (manual fix, alternative approach, or no change)

## References


- Project README: README.md
- Architecture Decision Record: ADR-0001 (in MODULE_3.md or TESTING.md)
- Test Strategy: TESTING.md
- Previous Module Evidence: VERIFICATION_REPORT.md
