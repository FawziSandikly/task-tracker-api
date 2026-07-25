# User Stories - Task Tracker Mid-Course Features

## Feature 1: Due Dates + Overdue Filter

### User Story 1.1: Add Due Date to New Task
**As a** project manager  
**I want to** set a due date when creating a task  
**So that** I can track deadlines and priorities

**Acceptance Criteria:**
- ✅ Due date field appears in task creation modal (optional)
- ✅ Valid ISO 8601 date format accepted (YYYY-MM-DD)
- ✅ Invalid date format rejected with clear error message
- ✅ Task created without due date still works (backward compatible)
- ✅ Due date persists in database and appears on task card

**AI Assumption Corrected:**
- Initial AI suggested storing as Unix timestamp; corrected to ISO 8601 string for frontend simplicity
- AI wanted to validate future-only dates; clarified to accept any valid date for flexibility

---

### User Story 1.2: View Overdue Tasks
**As a** project manager  
**I want to** see which tasks are overdue  
**So that** I can prioritize urgent work

**Acceptance Criteria:**
- ✅ Backend computes overdue status (due_date < today)
- ✅ Query parameter `/api/v1/tasks?filter=overdue` returns only overdue tasks
- ✅ Frontend displays overdue indicator (red badge or visual marker)
- ✅ Overdue tasks show due date prominently on card
- ✅ Filter parameter works independently and combined with status filter

**AI Assumption Corrected:**
- AI suggested client-side date comparison; moved to backend for consistency
- AI wanted to add priority field; kept scope focused on due dates only

---

### User Story 1.3: Update Task Due Date
**As a** team member  
**I want to** change a task's due date  
**So that** I can adjust timelines as priorities shift

**Acceptance Criteria:**
- ✅ Due date field editable in task update modal
- ✅ Can clear due date (set to null)
- ✅ Update without touching due date preserves existing date
- ✅ Invalid format rejected with 422 error
- ✅ Changes reflected immediately in UI

---

## Feature 2: Task Tags/Labels

### User Story 2.1: Create Task with Tags
**As a** team lead  
**I want to** add tags (e.g., "urgent", "documentation", "design") to tasks  
**So that** I can organize and filter work by category

**Acceptance Criteria:**
- ✅ Tags field accepts comma-separated values in creation modal
- ✅ Each tag trimmed of whitespace and validated (non-empty, 1-50 chars)
- ✅ Maximum 10 tags per task enforced with clear error
- ✅ Duplicate tags within same task rejected
- ✅ Tags displayed as chips/badges on task cards
- ✅ Tags persisted as normalized list in database

**AI Assumption Corrected:**
- AI suggested separate "tags" table with foreign keys; kept simple comma-separated field for this scope
- AI wanted case-insensitive tag matching; clarified to preserve case for simplicity

---

### User Story 2.2: Filter Tasks by Tag
**As a** team member  
**I want to** filter tasks by tag  
**So that** I can see all work related to a specific category

**Acceptance Criteria:**
- ✅ Query parameter `/api/v1/tasks?tag=urgent` filters by exact tag match
- ✅ Returns 200 with empty list if no matches
- ✅ Multiple tag filters work: `/api/v1/tasks?tag=urgent&tag=design` (AND logic)
- ✅ Frontend tag filter UI updates board dynamically
- ✅ Can combine with status and overdue filters

**AI Assumption Corrected:**
- AI suggested OR logic for multiple tags; specified AND logic (task must have all selected tags)
- AI wanted tag autocomplete; out of scope, user types manually

---

### User Story 2.3: Update and Manage Task Tags
**As a** team member  
**I want to** edit tags on existing tasks  
**So that** I can recategorize work without recreating tasks

**Acceptance Criteria:**
- ✅ Edit modal shows current tags as editable field
- ✅ Can add/remove tags without affecting other task properties
- ✅ Empty tag string clears all tags (no error)
- ✅ Validation same as creation (max 10, non-empty, 1-50 chars each)
- ✅ Update preserves tags if update payload omits tags field

---

## Summary of Scope Constraints

✅ **In Scope (Implemented):**
- Due dates as optional ISO 8601 strings
- Backend-computed overdue detection
- Query filtering by overdue status
- Tags as comma-separated validated list
- Tag filtering with AND logic
- Frontend UI updates for both features

❌ **Out of Scope (Explicitly Rejected):**
- Tag autocomplete suggestions
- Tag relationships or tag hierarchy
- Separate tag management interface
- Priority field (due dates sufficient for urgency)
- Calendar date picker (text input only)
- Bulk tag operations
- Tag creation workflow

---

## Testing Strategy

**Feature 1 Tests:**
1. Create task with valid due date
2. Create task with invalid date format → 422
3. Task without due date (null) works
4. Overdue filter returns only past-dated tasks
5. Update due date on existing task
6. Clear due date (set to null)

**Feature 2 Tests:**
1. Create task with valid tags
2. Reject empty tags
3. Reject more than 10 tags
4. Filter by single tag
5. Filter by multiple tags (AND logic)
6. Update tags without affecting other properties
7. Clear tags (empty string)

---

**Last Updated:** 2026-07-25  
**Status:** Ready for implementation