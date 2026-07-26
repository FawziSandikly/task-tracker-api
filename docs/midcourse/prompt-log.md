# Prompt Log

## Prompt 1 – Designing the API
**Goal:** Plan the REST API endpoints for a task tracker.

**Prompt:**
> Design a RESTful Task Tracker API with CRUD operations for tasks. Include endpoints, request bodies, and response examples.

**Outcome:**
Created the API structure with endpoints:
- GET /tasks
- GET /tasks/:id
- POST /tasks
- PUT /tasks/:id
- DELETE /tasks/:id

---

## Prompt 2 – Database Schema
**Goal:** Create a database model.

**Prompt:**
> Generate a SQL schema for a task tracker application with task title, description, status, priority, and due date.

**Outcome:**
Generated a `tasks` table with appropriate columns and constraints.

---

## Prompt 3 – Error Handling
**Goal:** Improve API reliability.

**Prompt:**
> Show best practices for handling errors in a Node.js Express REST API.

**Outcome:**
Added consistent HTTP status codes, validation, and error messages.

---

## Prompt 4 – Input Validation
**Goal:** Validate incoming requests.

**Prompt:**
> How can I validate task creation requests using Express Validator?

**Outcome:**
Implemented validation rules for required fields and invalid data.

---

## Prompt 5 – Testing
**Goal:** Test the API.

**Prompt:**
> Write Postman test cases for a Task Tracker API CRUD application.

**Outcome:**
Created test cases covering successful requests and common error scenarios.

---

## Lessons Learned

- More specific prompts produce more useful code.
- Asking for examples speeds up development.
- AI is helpful for debugging and documentation, but all generated code should be reviewed and tested.
