# Mid-Course Verification Report

## Project

Task Tracker REST API

---

# Objective

Verify that the two implemented mid-course features (Due Dates and Tags) work correctly and that invalid input is handled appropriately.

---

# Feature 1 — Due Dates

## Description

Tasks can optionally include a due date.

The due date is stored with each task and can be used to determine whether a task is overdue.

### Verification Performed

✓ Created a task with a due date.

Expected Result:
Task is created successfully.

Actual Result:
Task was created successfully.

Status:
PASS

---

✓ Updated a task with a different due date.

Expected Result:
The updated due date is saved.

Actual Result:
The new due date was returned by the API.

Status:
PASS

---

✓ Retrieved a task with a due date.

Expected Result:
The due date appears in the API response.

Actual Result:
The API returned the correct due date.

Status:
PASS

---

✓ Created a task without a due date.

Expected Result:
Task is accepted because due dates are optional.

Actual Result:
Task was created successfully.

Status:
PASS

---

# Feature 2 — Tags

## Description

Tasks support tags for organization.

### Verification Performed

✓ Created a task with tags.

Expected Result:
Tags are stored successfully.

Actual Result:
Tags were returned by the API.

Status:
PASS

---

✓ Updated task tags.

Expected Result:
Existing tags are replaced with the updated values.

Actual Result:
Updated tags were returned correctly.

Status:
PASS

---

✓ Retrieved tagged task.

Expected Result:
The API returns the assigned tags.

Actual Result:
Tags were returned correctly.

Status:
PASS

---

✓ Created task without tags.

Expected Result:
Task is accepted because tags are optional.

Actual Result:
Task created successfully.

Status:
PASS

---

# Break Tests

## Break Test 1

Attempted to create a task without a title.

Expected Result

HTTP 422 Validation Error

Actual Result

The API rejected the request with HTTP 422.

Status

PASS

---

## Break Test 2

Requested a task using an ID that does not exist.

Expected Result

HTTP 404 Not Found

Actual Result

The API returned HTTP 404.

Status

PASS

---

## Break Test 3

Attempted an invalid status transition.

Expected Result

HTTP 422 Validation Error.

Actual Result

The request was rejected.

Status

PASS

---

## Break Test 4

Submitted an invalid due date.

Expected Result

Validation error.

Actual Result

The request was rejected.

Status

PASS

---

## Break Test 5

Submitted invalid tag data.

Expected Result

Validation error.

Actual Result

The request was rejected.

Status

PASS

---

# Summary

Both mid-course features were successfully verified through manual testing and automated tests.

The verification confirmed that:

- Due dates are stored and returned correctly.
- Tags are stored and updated correctly.
- Invalid requests are rejected with appropriate HTTP error responses.
- Existing functionality continues to operate correctly after the addition of the new features.

Overall, the Task Tracker API satisfies the functional requirements for the implemented mid-course features.
