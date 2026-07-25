# Mini-ADR: Due Dates + Tags Implementation

**Date:** 2026-07-25  
**Branch:** mid-course-project  
**Status:** DECISION RECORDED

---

## Context

The Task Tracker needs two scoped features to demonstrate AI-assisted development workflow:

1. **Due Dates + Overdue Filter** - Track task deadlines and identify overdue work
2. **Task Tags/Labels** - Categorize tasks for organization and filtering

Must maintain backward compatibility, add comprehensive tests, and document the AI-assisted workflow.

---

## Decision: Feature 1 - Due Dates + Overdue Filter

### Option A (SELECTED): Backend-computed due dates with optional field
- Add `due_date: Optional[datetime]` to TaskTable and schemas
- Compute overdue in backend service layer: `due_date < datetime.utcnow()`
- Support query parameter filter: `GET /tasks?filter=overdue`
- Frontend displays due date badge; backend enforces date validation

**Rationale:**
- Single source of truth in backend (prevents client timezone issues)
- Consistent with existing backend validation pattern
- Easy to add more filters later (status + overdue combined queries)
- API documentation clear about what "overdue" means

**AI Suggestion Rejected:**
- "Store as Unix timestamp for efficiency" → Rejected: ISO 8601 string simpler for frontend
- "Validate only future dates" → Rejected: Accept any valid date for flexibility
- "Add priority field alongside due dates" → Rejected: Out of scope; due dates sufficient

### Option B (REJECTED): Client-side date computation
- Store due_date, client computes overdue in JavaScript
- **Problem:** Timezone mismatches, inconsistent filtering across clients
- **Problem:** Cannot efficiently query "all overdue tasks" from backend

### Option C (REJECTED): Separate DueDate model with foreign key
- Complex for this scope
- Adds unnecessary database join

---

### Implementation Details:

**Database Schema Change:**
```python
# app/models/task.py - Add to TaskTable
due_date: Optional[datetime] = Field(default=None, nullable=True)
```

**Schema Changes:**
```python
# app/schemas/task.py - Update schemas
class TaskCreate(BaseModel):
    due_date: Optional[str] = Field(None, description="ISO 8601 date string")

class TaskUpdate(BaseModel):
    due_date: Optional[str] = Field(None)

class TaskRead(BaseModel):
    due_date: Optional[str] = Field(None)
```

**Service Layer:**
```python
# app/services/task_service.py - Add
@staticmethod
def is_overdue(due_date: Optional[datetime]) -> bool:
    if not due_date:
        return False
    return due_date.date() < datetime.utcnow().date()

@staticmethod
def list_tasks_filtered(session: Session, filter_type: Optional[str] = None) -> list:
    tasks = TaskService.list_tasks(session)
    if filter_type == "overdue":
        return [t for t in tasks if TaskService.is_overdue(t.due_date)]
    return tasks
```

**API Endpoint:**
```python
# app/api/v1/endpoints/tasks.py - Modify GET /tasks
@router.get("/", response_model=list[TaskRead])
def list_tasks(session: Session = Depends(get_session), filter: Optional[str] = None):
    return TaskService.list_tasks_filtered(session, filter)
```

---

## Decision: Feature 2 - Task Tags/Labels

### Option A (SELECTED): Comma-separated string field with validation
- Add `tags: str` to TaskTable (default="")
- Validate as comma-separated list in schema
- Parse/split in service layer
- Store normalized (trimmed, deduplicated)

**Rationale:**
- No schema migration complexity (single field)
- Simple to query: use LIKE or direct string comparison
- Backward compatible (empty string for no tags)
- Sufficient for learning scope

**AI Suggestion Rejected:**
- "Create separate Tag model and many-to-many relationship" → Rejected: Over-engineered for this scope
- "Use PostgreSQL array type" → Rejected: Staying with SQLite compatibility
- "Implement tag hierarchy with parent/child" → Rejected: Out of scope
- "Add tag autocomplete with existing tags list" → Rejected: Frontend complexity; manual entry sufficient

### Option B (REJECTED): Separate normalized Tags table
- Complex migration
- Requires JOIN queries
- Not necessary for MVP scope

### Option C (REJECTED): JSON field
- SQLite doesn't have native JSON; would need string storage anyway
- Comma-separated simpler to understand

---

### Implementation Details:

**Database Schema Change:**
```python
# app/models/task.py - Add to TaskTable
tags: str = Field(default="")  # comma-separated, normalized
```

**Schema Changes:**
```python
# app/schemas/task.py - Update schemas
class TaskCreate(BaseModel):
    tags: Optional[str] = Field(None, description="Comma-separated tag list")

class TaskUpdate(BaseModel):
    tags: Optional[str] = Field(None)

class TaskRead(BaseModel):
    tags: str = Field(default="")
```

**Service Layer Validation:**
```python
# app/services/task_service.py - Add
@staticmethod
def validate_and_normalize_tags(tags_str: Optional[str]) -> str:
    if not tags_str:
        return ""
    
    # Split, trim, filter empty
    tags = [t.strip() for t in tags_str.split(",") if t.strip()]
    
    # Validate: max 10, each 1-50 chars
    if len(tags) > 10:
        raise HTTPException(status_code=422, detail="Maximum 10 tags per task")
    
    for tag in tags:
        if len(tag) < 1 or len(tag) > 50:
            raise HTTPException(status_code=422, detail=f"Tag '{tag}' must be 1-50 characters")
    
    # Remove duplicates, rejoin
    return ", ".join(sorted(set(tags)))
```

**API Endpoint:**
```python
# app/api/v1/endpoints/tasks.py - Modify GET /tasks
@router.get("/", response_model=list[TaskRead])
def list_tasks(
    session: Session = Depends(get_session),
    filter: Optional[str] = None,
    tag: Optional[List[str]] = Query(None)
):
    if filter == "overdue":
        tasks = TaskService.list_tasks_filtered(session, "overdue")
    else:
        tasks = TaskService.list_tasks(session)
    
    if tag:
        tasks = [t for t in tasks if all(tag_val in t.tags for tag_val in tag)]
    
    return tasks
```

---

## Frontend Implementation Strategy

### Feature 1: Due Dates
1. Add `due_date` input field to task creation modal
2. Display due date on task card (e.g., "Due: 2026-08-15")
3. Show overdue badge (red) if past due
4. Add overdue filter checkbox above board
5. Update card rendering to show due date or overdue status

### Feature 2: Tags
1. Add `tags` textarea or comma-separated input to modal
2. Render tags as colored chips/badges on card
3. Add tag filter buttons or search box
4. Highlight selected tag filters
5. Show "No tags" text if empty

---

## Testing Strategy

**Backend Tests (pytest):**
- 6-8 new tests for due dates (validation, filtering, update)
- 6-8 new tests for tags (validation, filtering, empty handling)
- All existing tests remain passing
- Total: 15 baseline + 12-16 new = 27-31 tests

**Frontend Testing (Manual + Browser):**
- Create task with due date
- See due date on card
- Filter by overdue
- Create task with tags
- See tags as chips
- Filter by tag

**Break Tests:**
- Set due_date to null, verify no crash
- Set invalid tag count (> 10), verify 422
- Combine filters: status=done + filter=overdue

---

## Alternatives Considered and Rejected

| Alternative | Why Rejected |
|-------------|----------|
| Nested Tag model with ForeignKey | Over-engineered; simple comma-separated sufficient |
| Client-side overdue computation | Timezone issues; backend is single source of truth |
| Priority field instead of due dates | Due dates more actionable; both out of scope for now |
| Calendar date picker UI component | Text input sufficient; picker adds complexity |
| Tag autocomplete from existing tags | Frontend complexity; manual entry sufficient |
| Separate notification system for overdue | Out of scope; visual indicator sufficient |
| Bulk operations (multi-select + tag) | Out of scope; single task operations only |

---

## Risk Mitigation

| Risk | Mitigation |
|------|--------|
| Breaking existing tests | Run full suite after each change; only add optional fields |
| Timezone bugs with due dates | Use UTC in backend; ISO 8601 strings; tests use UTC |
| Invalid tag input crashing UI | Comprehensive validation in schema + service layer |
| Performance with tag filtering | In-memory filtering acceptable for small task counts |
| Database migration issues | Keep as nullable fields; no data loss |

---

## Success Criteria

✅ Both features implemented end-to-end (backend + frontend + tests)  
✅ All 15 baseline tests still pass  
✅ 12-16 new tests added and passing  
✅ Backward compatible (no breaking changes)  
✅ AI workflow documented with prompts and decisions  
✅ Code follows existing patterns (TaskService layer, Pydantic validation)  
✅ Frontend updated with new fields visible on cards  

---

**Decision Authority:** Mid-course Project Requirements  
**Implementation Owner:** Using AI-assisted workflow  
**Status:** APPROVED FOR IMPLEMENTATION