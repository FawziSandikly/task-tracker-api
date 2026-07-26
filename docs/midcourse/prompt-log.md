# Prompt Log

## Project

Task Tracker REST API

---

## Prompt 1 – Design Due Date Feature

**Goal**

Design a feature that allows tasks to have optional due dates and support overdue task filtering.

**Prompt**

> Design a FastAPI implementation for adding optional due dates to a Task Tracker API using SQLModel. Include validation and an overdue filter.

**Outcome**

The response provided a clean approach for adding an optional `due_date` field, updating the database model, and implementing logic for identifying overdue tasks.

---

## Prompt 2 – Implement Tags

**Goal**

Allow tasks to be organized using tags.

**Prompt**

> Show how to add tags to tasks in a FastAPI Task Tracker API. Include model changes and CRUD support.

**Outcome**

The response suggested storing tags with each task and updating the API so tags could be created, updated, and returned in responses.

---

## Prompt 3 – Status Validation

**Goal**

Validate task status transitions.

**Prompt**

> Implement validation so task status can only move from todo → in_progress → done.

**Outcome**

The generated solution helped implement transition rules while preventing invalid backward transitions.

---

## Prompt 4 – API Testing

**Goal**

Improve automated testing.

**Prompt**

> Write pytest tests for CRUD operations, status transitions, and invalid requests in a FastAPI Task Tracker API.

**Outcome**

Additional unit tests were added for successful requests and common error conditions.

---

## Prompt 5 – Documentation

**Goal**

Improve project documentation.

**Prompt**

> Generate documentation describing the implemented API features, usage examples, and testing strategy.

**Outcome**

The generated documentation served as a starting point for the README and project reports.

---

# Lessons Learned

- Specific prompts produced more accurate responses.
- AI accelerated implementation and debugging.
- Generated code was reviewed and modified before being committed.
- Documentation quality improved by iteratively refining prompts.
