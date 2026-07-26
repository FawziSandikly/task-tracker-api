# Midcourse Verification Report

## Project

Task Tracker API

## Features Verified

### Feature 1: Create and Manage Tasks

**Expected Behavior**
- Users can create a new task.
- Users can retrieve tasks.
- Users can update task details.
- Users can delete tasks.

**Verification**
| Test | Result |
|------|--------|
| Create task | ✅ Passed |
| Get task | ✅ Passed |
| Update task | ✅ Passed |
| Delete task | ✅ Passed |

---

### Feature 2: Task Status Management

**Expected Behavior**
- Users can mark tasks as Pending, In Progress, or Completed.

**Verification**
| Test | Result |
|------|--------|
| Set Pending | ✅ Passed |
| Set In Progress | ✅ Passed |
| Set Completed | ✅ Passed |

---

# Break Tests

## Break Test 1: Missing Title

**Request**

```json
{
  "description": "Finish assignment"
}
```

**Expected Result**

HTTP 400 Bad Request

**Actual Result**

Returned HTTP 400 with validation error.

✅ Passed

---

## Break Test 2: Invalid Task ID

**Request**

```
GET /tasks/9999
```

**Expected Result**

HTTP 404 Not Found

**Actual Result**

Returned HTTP 404.

✅ Passed

---

## Break Test 3: Invalid Status

**Request**

```json
{
  "status": "Finished"
}
```

**Expected Result**

HTTP 400 Bad Request

**Actual Result**

Returned validation error.

✅ Passed

---

# Summary

All implemented mid-course features behaved as expected during testing. Normal functionality passed, and invalid inputs were correctly rejected with appropriate HTTP error responses.
