# User Stories

## Feature: Due Dates

### User Story 1

**As a user,**
I want to assign a due date to a task,
**so that**
I know when it should be completed.

---

### Acceptance Criteria

- Users can provide an optional due date.
- Due dates are stored with the task.
- Due dates are returned in API responses.

---

## User Story 2

**As a user,**
I want to identify overdue tasks,
**so that**
I can prioritize unfinished work.

---

### Acceptance Criteria

- Tasks with past due dates are considered overdue.
- Completed tasks are not considered overdue.
- Tasks without due dates are not marked overdue.

---

# Feature: Tags

## User Story 3

**As a user,**
I want to assign tags to tasks,
**so that**
I can organize similar tasks together.

---

### Acceptance Criteria

- Tasks can have one or more tags.
- Tags are optional.
- Tags are returned by the API.

---

## User Story 4

**As a user,**
I want to update the tags assigned to a task,
**so that**
I can reorganize my tasks whenever needed.

---

### Acceptance Criteria

- Existing tags can be modified.
- Empty tags are allowed.
- Updated tags are saved correctly.

---

## User Story 5

**As a user,**
I want to filter tasks using tags,
**so that**
I can quickly find related work.

---

### Acceptance Criteria

- Users can request tasks matching a tag.
- Only matching tasks are returned.
- Filtering does not modify stored data.

---

# Summary

The Due Dates feature improves task scheduling by allowing deadlines and overdue tracking.

The Tags feature improves organization by allowing tasks to be grouped and filtered according to user-defined labels.
