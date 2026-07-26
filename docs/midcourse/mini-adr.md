# Mini Architecture Decision Record

## ADR-0002: Add Due Dates and Tags to Tasks

**Status:** Accepted

**Date:** July 2026

---

## Context

The original Task Tracker API allowed users to create, update, and manage tasks with a title, description, and status. However, users had no way to assign deadlines or organize tasks into categories.

To improve task management, two new features were required:

- Due Dates
- Tags

These features should integrate with the existing FastAPI and SQLModel architecture while keeping the API simple and backward compatible.

---

## Decision

The project was extended with support for optional due dates and tags.

### Due Dates

Each task can optionally include a `due_date`.

This allows users to:

- Schedule work
- Track deadlines
- Identify overdue tasks

Tasks without a due date continue to work exactly as before.

---

### Tags

Each task can contain one or more tags.

Tags allow users to organize tasks into logical groups such as:

- work
- school
- personal
- urgent

Tags are optional and can be updated after task creation.

---

## Consequences

### Advantages

- Better task organization.
- Easier task prioritization.
- Support for deadline tracking.
- Improved API usability.
- Backward compatibility with existing clients.

### Disadvantages

- Additional validation logic.
- More complex database model.
- Additional testing required.

---

## Alternatives Considered

### Separate Categories Table

Rejected because the project requirements only required lightweight organization.

### Required Due Dates

Rejected because many tasks do not need deadlines.

### Fixed Tag List

Rejected because users should be free to create their own tags.

---

## Decision Summary

Adding Due Dates and Tags improves the usability of the Task Tracker API while maintaining a clean REST architecture and preserving compatibility with existing functionality.
