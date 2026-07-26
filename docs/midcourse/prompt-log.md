# Prompt Log

## Project
Task Tracker REST API

This document records the prompts used during the development of the mid-course features and how they contributed to the implementation.

---

## Prompt 1

### Goal
Implement Due Dates for tasks.

### Prompt
Design a FastAPI implementation that adds an optional due_date field to a Task Tracker API built with SQLModel. Include validation and explain how overdue tasks should be determined.

### Outcome
The response explained how to:
- Add a due_date field to the SQLModel model.
- Update request and response schemas.
- Store due dates in SQLite.
- Compare due dates against the current date to determine whether a task is overdue.

The generated code was reviewed and adapted before being added to the project.

---

## Prompt 2

### Goal
Implement Tags.

### Prompt
Show how to add tags to a Task Tracker API so each task can store multiple tags and return them in API responses.

### Outcome
The response explained how to:
- Store tags with each task.
- Update the schemas.
- Return tags from the API.
- Support updating tags.

The generated solution required minor modifications before integration.

---

## Prompt 3

### Goal
Improve automated testing.

### Prompt
Write pytest tests for a FastAPI Task Tracker API including CRUD operations, due dates, tags, and invalid input handling.

### Outcome
The response generated example unit tests that were modified to match the project structure before being committed.

---

## Prompt 4

### Goal
Debug API validation.

### Prompt
Why does my FastAPI endpoint return HTTP 422 instead of HTTP 200 when updating a task?

### Outcome
The explanation helped identify validation issues and improve request handling.

---

## Prompt 5

### Goal
Improve project documentation.

### Prompt
Generate documentation explaining the new features, API endpoints, and testing strategy.

### Outcome
The generated documentation was used as a starting point for updating the README and project reports.

---

# Reflection on AI Usage

AI significantly reduced development time by helping explain concepts, generate example code, and debug problems. All generated code was reviewed, tested, and modified before being merged into the project.

The most useful prompts were the ones that included project-specific details rather than general programming questions.
