# MODULE 3: AI-Assisted Coding with GitHub Copilot

## Overview
This module teaches AI-assisted coding using GitHub Copilot to enhance, test, and refactor the Task Tracker API. Focus on the iterative workflow: **ask → inspect → run → test → refine**.

---

## Core Reading 1: GitHub Docs - Best Practices for Using GitHub Copilot

**Link:** [GitHub Copilot Best Practices](https://docs.github.com/en/copilot/using-github-copilot/best-practices-for-using-github-copilot)

### Key Concepts for Task Tracker

#### 1. Creating Thoughtful Prompts
Instead of: `\"Write a test\"`
Use: `\"Write a pytest test that verifies invalid status transitions (done → in_progress) return HTTP 422 and leave the task unchanged\"`

**Example in Task Tracker context:**
```python
# ❌ Vague prompt
# \"Write validation code\"

# ✅ Specific prompt
# \"Write validation code that checks if a task status transition from 'done' to 'in_progress' 
#  is allowed per ADR-0001, and raise HTTPException with status 422 if invalid\"
```

#### 2. Breaking Down Complex Tasks
For refactoring the frontend Kanban board:
1. First: Ask about drag-and-drop event structure
2. Second: Ask about fetching updated status after drop
3. Third: Ask about error handling when API returns 422

**Task Tracker Example:**
```
Task: Add Kanban board view to frontend
Step 1: Generate HTML structure with todo/in_progress/done columns
Step 2: Generate JavaScript drag-and-drop event handlers
Step 3: Generate fetch calls to PATCH endpoint when task is dropped
Step 4: Generate error handling for invalid transitions
```

#### 3. Providing Examples
When asking Copilot to generate code, show the existing pattern first:

```python
# Show Copilot the existing health endpoint
@router.get(\"/health\", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status=\"healthy\", message=\"Task Tracker API is running\")

# Then ask: \"Generate similar endpoint pattern for /stats that returns task counts by status\"
```

#### 4. Checking Copilot's Work
Always verify generated code:
- ✅ Follows ADR-0001 transition rules
- ✅ Uses correct HTTP status codes (200, 404, 422)
- ✅ Includes docstrings and inline comments
- ✅ Matches existing code style
- ✅ Passes pytest tests

#### 5. Using Tests to Validate Suggestions
Run tests after each suggestion:
```bash
# After Copilot generates code
pytest -v tests/test_tasks.py::test_invalid_transition_done_to_in_progress

# If it passes, integration test in browser
# If it fails, ask Copilot: \"This test failed with [error]. Fix it.\"
```

---

## Core Reading 2: GitHub Docs - Asking GitHub Copilot Questions in Your IDE

**Link:** [Asking GitHub Copilot Questions in Your IDE](https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide)

### Workflow: Ask from Inside the IDE (Not Generic Chat)

#### Step 1: Open Task Tracker Repo Locally
```bash
git clone https://github.com/FawziSandikly/task-tracker-api.git
cd task-tracker-api
code .  # Open in VS Code with GitHub Copilot installed
```

#### Step 2: Use IDE Chat (Copilot Chat in VS Code)
- Open Copilot Chat with `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Shift+I` (Mac)
- Copilot now has context of your actual codebase

#### Step 3: Ask Context-Specific Questions
**Good questions to ask Copilot:**

1. **About existing code:**
   ```
   \"Explain what TaskService.validate_transition does and how it enforces ADR-0001 rules\"
   ```

2. **About file relationships:**
   ```
   \"Show me the flow from POST /tasks/ endpoint through TaskService to TaskTable model\"
   ```

3. **About specific patterns:**
   ```
   \"Why does TaskUpdate have all Optional fields instead of required fields?\"
   ```

4. **About testing:**
   ```
   \"Generate a test that verifies a task status update with invalid transition returns 422 
   and the database task remains unchanged\"
   ```

#### Step 4: Provide File Context
Instead of asking vaguely, select code first:

**Task Tracker Example:**
1. Open `app/services/task_service.py`
2. Select the `update_task` method
3. Ask: \"Why does validation happen before applying changes?\"
4. Copilot explains the atomic validation pattern

#### Step 5: Smart Actions
In VS Code with Copilot:
- Select a line → Right-click → \"Copilot\" → \"Explain\"
- Select code → Right-click → \"Copilot\" → \"Generate Tests\"
- Select function → Right-click → \"Copilot\" → \"Fix Issues\"

---

## Core Reading 3: VS Code Docs - Inline Chat

**Link:** [VS Code Inline Chat](https://code.visualstudio.com/docs/editor/inlinechat)

### Using Inline Chat for Targeted Refactoring

#### Scenario 1: Fix a Specific Endpoint

**Without inline chat (bad):**
- Ask for entire file rewrite
- Get 500 lines of code
- Hard to review changes

**With inline chat (good):**
1. Open `app/api/v1/endpoints/tasks.py`
2. Select just the `update_task` function
3. Press `Ctrl+I` (inline chat shortcut)
4. Ask: \"Add validation that title is not empty\"
5. Review the inline diff with Keep/Undo buttons

#### Scenario 2: Refactor Task Status Validation

```python
# Select this code block in task_service.py
if new_status not in ALLOWED_TRANSITIONS[current_status]:
    allowed = \", \".join([s.value for s in ALLOWED_TRANSITIONS[current_status]])
    raise HTTPException(
        status_code=422,
        detail=f\"Invalid transition from '{current_status.value}' to '{new_status.value}'. Allowed transitions: {allowed}\"
    )

# Then: Press Ctrl+I and ask
# \"Generate a helper method that returns a human-readable message of allowed transitions\"
```

#### Inline Chat Workflow for Task Tracker

1. **Open file** in VS Code
2. **Select code block** you want to change
3. **Press `Ctrl+I`** to open inline chat
4. **Type focused prompt** (not full file rewrites)
5. **Review diff** that appears inline
6. **Keep** the changes or **Undo**
7. **Save and test** with `pytest`

**Examples:**

**Example 1: Improve error message**
```python
# Select validation code
if task_update.status and task_update.status != db_task.status:
    TaskService.validate_transition(db_task.status, task_update.status)

# Inline chat: \"Make error message include which fields caused the validation failure\"
```

**Example 2: Add logging**
```python
# Select create_task method
# Inline chat: \"Add logging at INFO level when a task is created\"
```

**Example 3: Fix edge case**
```python
# Select the partial update logic
# Inline chat: \"Handle the case where description is empty string vs None\"
```

---

## Core Reading 4: MDN - HTML Drag and Drop API

**Link:** [MDN HTML Drag and Drop API](https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API)

### Building Kanban Board with Native Drag-and-Drop

**Why native drag-and-drop? Not a library?**
- Task Tracker is a learning project
- Native API teaches core browser concepts
- No external dependencies
- Perfect for understanding event lifecycle

### Key Concepts for Kanban Board

#### 1. Draggable Items
```html
<!-- In frontend/kanban.html -->
<div class=\"task-item\" draggable=\"true\" data-task-id=\"1\">
  <h3>Buy groceries</h3>
  <p>Status: To Do</p>
</div>
```

#### 2. Drag Events Sequence
1. **dragstart** - User starts dragging (store task ID)
2. **dragover** - Moving over drop target (allow drop)
3. **drop** - User releases on target (send API request)

```javascript
// dragstart: Store which task is being moved
element.addEventListener('dragstart', (e) => {
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('taskId', element.dataset.taskId);
});

// dragover: Allow drop on column
column.addEventListener('dragover', (e) => {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
});

// drop: Update status and call API
column.addEventListener('drop', async (e) => {
  const taskId = e.dataTransfer.getData('taskId');
  const newStatus = column.dataset.status;
  await updateTaskStatus(taskId, newStatus);
});
```

#### 3. DataTransfer Object
- `setData(format, value)` - Store data (task ID)
- `getData(format)` - Retrieve data on drop
- `dropEffect = 'move'` - Show move cursor
- `effectAllowed = 'move'` - Allow move operation

---

## Core Reading 5: MDN - Using the Fetch API

**Link:** [MDN Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)

### Critical for Task Tracker Frontend

#### Why This Matters
FastAPI returns 404 or 422, but **fetch does NOT automatically reject the promise**.
Your code MUST check `.ok` or `.status`.

#### Pattern 1: Sending JSON (POST)
```javascript
// Create task
const response = await fetch('http://localhost:8000/api/v1/tasks/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'My task', description: 'Details' })
});

if (!response.ok) {
  const error = await response.json();
  console.error('Create failed:', error.detail);
  return;
}

const task = await response.json();
console.log('Created:', task);
```

#### Pattern 2: Updating JSON (PATCH)
```javascript
// Update task status
const response = await fetch(`http://localhost:8000/api/v1/tasks/${taskId}`, {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ status: 'in_progress' })
});

if (!response.ok) {
  const error = await response.json();
  // Handle 422 (invalid transition)
  if (response.status === 422) {
    alert(`Cannot change status: ${error.detail}`);
  }
  return;
}

const updated = await response.json();
console.log('Updated:', updated);
```

#### Pattern 3: Error Handling for 404/422
```javascript
async function updateTaskStatus(taskId, newStatus) {
  try {
    const response = await fetch(
      `http://localhost:8000/api/v1/tasks/${taskId}`,
      {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      }
    );

    // CRITICAL: Check response.ok or response.status
    if (response.status === 404) {
      alert('Task not found');
      reloadTasks(); // Refresh list
      return;
    }

    if (response.status === 422) {
      const error = await response.json();
      alert(`Invalid transition: ${error.detail}`);
      reloadTasks(); // Refresh to reset UI
      return;
    }

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const task = await response.json();
    console.log('Task updated:', task);
    reloadTasks(); // Refresh board
  } catch (error) {
    console.error('Error:', error);
  }
}
```

#### Pattern 4: Reading JSON Responses
```javascript
// Always check status BEFORE calling .json()
async function fetchTasks() {
  try {
    const response = await fetch('http://localhost:8000/api/v1/tasks/');

    if (!response.ok) {
      throw new Error(`Failed to fetch tasks: ${response.status}`);
    }

    const tasks = await response.json();
    return tasks; // Array of task objects
  } catch (error) {
    console.error('Fetch error:', error);
    return [];
  }
}
```

---

## Core Reading 6: GitHub Docs - Writing Tests with GitHub Copilot

**Link:** [GitHub Docs - Writing Tests with GitHub Copilot](https://docs.github.com/en/copilot/using-github-copilot/writing-tests-with-github-copilot)

### Copilot Chat Testing Workflow for Task Tracker

#### Step 1: Ask Copilot to Brainstorm Tests
Open Copilot Chat (`Ctrl+Shift+I`) and ask:

```
\"I have a TaskService.update_task method that validates status transitions per ADR-0001.
Generate a list of edge-case tests I should write:
1. Valid transitions
2. Invalid transitions
3. Partial updates
4. Database consistency
\"
```

Copilot will suggest test scenarios.

#### Step 2: Ask Copilot to Draft a Test
Select the `task_service.py` file and ask:

```
\"Generate a pytest test that verifies when a task is in 'done' status,
attempting to transition to 'in_progress' returns HTTP 422 and the task remains unchanged.
Use the TestClient fixture from conftest.py.\"
```

#### Step 3: Review the Generated Test
Copilot generates test code. **YOU verify it:**

```python
# ✅ Check this was generated correctly:
# - Uses client fixture
# - Creates task in 'done' status
# - Attempts invalid transition
# - Asserts response.status_code == 422
# - Asserts task in database is still 'done'
```

#### Step 4: Run the Test
```bash
pytest tests/test_tasks.py::test_invalid_transition_done_to_in_progress -v
```

#### Step 5: Refine if Needed
If the test fails:
```
\"This test failed with: [error message]
Fix the test to [description of what went wrong]\"
```

### Example: Copilot Test Generation for Task Tracker

**Prompt:**
```
\"Generate a pytest test that creates a task, updates it to 'in_progress',
then attempts to move it back to 'todo'. It should:
1. Verify the response is 422 Unprocessable Entity
2. Verify the error message mentions 'Invalid transition'
3. Fetch the task again and verify it's still 'in_progress' in the database\"
```

**Copilot generates:**
```python
def test_invalid_transition_in_progress_to_todo(client: TestClient):
    # Create task
    create_response = client.post(
        \"/api/v1/tasks/\",
        json={\"title\": \"Task\", \"status\": \"in_progress\"}
    )
    task_id = create_response.json()[\"id\"]

    # Try invalid transition
    response = client.patch(
        f\"/api/v1/tasks/{task_id}\",
        json={\"status\": \"todo\"}
    )

    # Verify 422
    assert response.status_code == 422
    assert \"Invalid transition\" in response.json()[\"detail\"]

    # Verify database unchanged
    get_response = client.get(f\"/api/v1/tasks/{task_id}\")
    assert get_response.json()[\"status\"] == \"in_progress\"
```

**YOU verify:**
- ✅ Uses fixtures correctly
- ✅ Tests the specific behavior
- ✅ Checks database state
- ✅ Matches ADR-0001 requirements

---

## Practical Reference 1: FastAPI - Testing

**Link:** [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

### Key Patterns for Task Tracker Tests

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# POST endpoint test
def test_create_task(client: TestClient):
    response = client.post(
        \"/api/v1/tasks/\",
        json={\"title\": \"Learn FastAPI\", \"description\": \"Complete the tutorial\"}
    )
    assert response.status_code == 200
    assert response.json()[\"status\"] == \"todo\"

# GET endpoint test
def test_get_task(client: TestClient):
    response = client.get(\"/api/v1/tasks/1\")
    assert response.status_code == 200

# Error case test
def test_task_not_found(client: TestClient):
    response = client.get(\"/api/v1/tasks/999\")
    assert response.status_code == 404
```

### Test Naming Convention
- `test_` prefix required
- Describe what is being tested
- Include expected result

**Examples:**
- ✅ `test_create_task_with_valid_title`
- ✅ `test_invalid_transition_done_to_in_progress`
- ✅ `test_update_preserves_status_when_omitted`
- ❌ `test_it` (unclear)
- ❌ `test_endpoint` (too vague)

---

## Practical Reference 2: pytest - Documentation

**Link:** [pytest Documentation](https://docs.pytest.org/)

### Running Specific Tests

```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_tasks.py

# Run specific test
pytest tests/test_tasks.py::test_create_task -v

# Run tests matching a pattern
pytest -k \"transition\" -v

# Run with coverage
pytest --cov=app --cov-report=html tests/

# Run and stop on first failure
pytest -x

# Run last 5 failed tests
pytest --lf -v
```

### Reading pytest Output

```
tests/test_tasks.py::test_create_task PASSED                          [10%]
tests/test_tasks.py::test_invalid_transition_done_to_in_progress FAILED [15%]

FAILED tests/test_tasks.py::test_invalid_transition_done_to_in_progress - AssertionError: assert 200 == 422
```

**Reading this:**
- Test file: `test_tasks.py`
- Test function: `test_invalid_transition_done_to_in_progress`
- Status: `FAILED`
- Error: Expected 422 but got 200

---

## Practical Reference 3: MDN - DataTransfer

**Link:** [MDN DataTransfer](https://developer.mozilla.org/en-US/docs/Web/API/DataTransfer)

### For Drag-and-Drop Implementation

```javascript
// In dragstart handler
event.dataTransfer.effectAllowed = 'move'; // User sees \"move\" cursor
event.dataTransfer.setData('text/plain', taskId); // Store task ID

// In drop handler
const taskId = event.dataTransfer.getData('text/plain'); // Retrieve task ID
event.dataTransfer.dropEffect = 'move'; // Confirm move happened

// Key properties:
// - effectAllowed: 'move', 'copy', 'link', 'none'
// - dropEffect: 'move', 'copy', 'link', 'none'
// - setData(format, value): Store data
// - getData(format): Retrieve data
```

---

## Practical Reference 4: VS Code Docs - Manage Context for AI

**Link:** [VS Code - Manage Context for AI](https://code.visualstudio.com/docs/copilot/managing-copilot-context)

### Making Copilot Understand Task Tracker

When Copilot gives generic answers, add context:

#### Method 1: Add Files to Chat
1. Open Copilot Chat
2. Click `+` to add files
3. Select:
   - `app/schemas/task.py`
   - `app/services/task_service.py`
   - `app/models/task.py`
4. Now ask: \"Explain the request/response flow for updating task status\"

#### Method 2: Select Code Before Asking
1. Open `app/services/task_service.py`
2. Select the `update_task` method
3. Ask Copilot (inline or chat): \"Why does validation happen before database changes?\"

#### Method 3: Reference Terminal Output
```bash
pytest tests/test_tasks.py -v
# Tests fail with specific error
```

Copy the error output into Copilot Chat:
```
I got this error when running tests:

[paste error output]

Fix the code to handle this edge case.
```

#### Method 4: Add Symbols to Context
If asking about a specific class or function:
```
\"Look at the TaskService class and the validate_transition method.
Generate a test that verifies all allowed transitions per ADR-0001.\"
```

---

## Module 3 Workflow: Complete AI-Assisted Coding Cycle

### Scenario: Add Kanban Board View to Frontend

#### Phase 1: Ask (Gathering Requirements)
**In Copilot Chat with frontend files selected:**
```
\"I need to add a Kanban board view to the Task Tracker frontend with columns for 
todo, in_progress, and done. Tasks should be draggable between columns and update 
the backend when moved. Generate the HTML structure with data attributes, 
CSS for a three-column layout, and JavaScript drag-and-drop handlers.\"
```

#### Phase 2: Inspect (Review Copilot's Response)
Copilot generates HTML/CSS/JavaScript. **You check:**
- ✅ Uses native drag-and-drop (not library)
- ✅ Stores task ID in `data-task-id` attribute
- ✅ Calls PATCH endpoint when dropped
- ✅ Handles 422 errors (invalid transitions)
- ✅ Matches existing frontend style

#### Phase 3: Run (Test Locally)
```bash
# Terminal 1: Start backend
uvicorn app.main:app --reload

# Terminal 2: Start frontend
cd frontend
python -m http.server 5173

# Browser: Open http://localhost:5173
# Test: Drag task from \"To Do\" to \"In Progress\"
```

#### Phase 4: Test (Run Automated Tests)
```bash
# Test backend
pytest tests/test_tasks.py::test_valid_transition_todo_to_in_progress -v

# Check frontend error handling
# Manually test moving task from \"Done\" to \"In Progress\" (should fail with 422)
```

#### Phase 5: Refine (Improve Based on Results)
If tests fail or UX is poor:
```
\"The drag-and-drop works but users can't see visual feedback. 
Add CSS classes that highlight drop zones while dragging over them.\"
```

---

## Testing Checklist for Module 3

### Backend Tests (pytest)
- [ ] All 15 tests in `tests/test_tasks.py` pass
- [ ] All 1 test in `tests/test_health.py` passes
- [ ] Coverage >= 90%
- [ ] Status transition validation works (valid and invalid)
- [ ] Partial updates preserve omitted fields
- [ ] Database errors return correct HTTP status codes

### Frontend Tests (Manual)
- [ ] Create task form works
- [ ] Task list displays all tasks
- [ ] Click task to view details
- [ ] Update task title/description
- [ ] Change status with dropdown
- [ ] Valid transitions allowed
- [ ] Invalid transitions show error message
- [ ] Delete task removes from list
- [ ] Drag-and-drop moves tasks between columns
- [ ] Dropping on invalid transition shows 422 error

### Integration Tests
- [ ] Backend runs with `uvicorn app.main:app --reload`
- [ ] Frontend connects to `http://localhost:8000/api/v1`
- [ ] CORS allows cross-origin requests
- [ ] No browser console errors
- [ ] No FastAPI errors in terminal

---

## Best Practices Summary

### Using GitHub Copilot for Task Tracker

1. **Be Specific**: \"Generate a test for invalid status transition\" → \"Generate a pytest test that verifies a task in 'done' status cannot transition to 'in_progress', returns 422, and database is unchanged\"

2. **Provide Context**: Select files/code before asking, use inline chat for targeted changes

3. **Verify Generated Code**: Run tests, check for ADR-0001 compliance, inspect error handling

4. **Use Tests to Validate**: After Copilot generates code, immediately run `pytest` to verify

5. **Break Complex Tasks**: Don't ask for \"full refactor\"; ask for components step-by-step

6. **Check Fetch Patterns**: Always check `.ok` or `.status` in fetch calls before parsing JSON

7. **Use Inline Chat**: For refactoring specific methods, not full file rewrites

8. **Add Terminal Context**: Copy error messages into chat to help Copilot fix issues

---

## Resources

**Core Readings:**
- [GitHub Copilot Best Practices](https://docs.github.com/en/copilot/using-github-copilot/best-practices-for-using-github-copilot)
- [Asking GitHub Copilot Questions in Your IDE](https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide)
- [VS Code Inline Chat](https://code.visualstudio.com/docs/editor/inlinechat)
- [MDN HTML Drag and Drop API](https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API)
- [MDN Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- [GitHub Copilot Testing](https://docs.github.com/en/copilot/using-github-copilot/writing-tests-with-github-copilot)

**Practical References:**
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [MDN DataTransfer](https://developer.mozilla.org/en-US/docs/Web/API/DataTransfer)
- [VS Code AI Context Management](https://code.visualstudio.com/docs/copilot/managing-copilot-context)

---

## Next Steps

1. **Read** Core 1 & 2 (Best practices, IDE prompting)
2. **Watch** IDE inline chat demo (Core 3)
3. **Build** Kanban board with Copilot assistance (Core 4 & 5)
4. **Write** edge-case tests with Copilot (Core 6)
5. **Test** all functionality with provided test commands
6. **Refine** based on test results and feedback
",
  "message": "Add Module 3: AI-Assisted Coding with GitHub Copilot - Complete Core and Practical Readings",
  "owner": "FawziSandikly",
  "path": "MODULE_3.md",
  "repo": "task-tracker-api"
}
