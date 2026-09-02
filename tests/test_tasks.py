# Tests for task CRUD endpoints, status transitions, due dates, and tags

from fastapi.testclient import TestClient
from app.schemas.task import TaskStatus

def test_create_task(client: TestClient):
"""Test creating a new task with default status"""
response = client.post(
"/api/v1/tasks/",
json={"title": "Buy groceries", "description": "Milk, eggs, bread"}
)

```
assert response.status_code == 200
data = response.json()
assert data["title"] == "Buy groceries"
assert data["status"] == TaskStatus.TODO.value
assert data["id"] is not None
```

def test_list_tasks_empty(client: TestClient):
"""Test listing tasks when database is empty"""
response = client.get("/api/v1/tasks/")

```
assert response.status_code == 200
assert response.json() == []
```

def test_list_tasks_with_data(client: TestClient):
"""Test listing tasks after creating multiple tasks"""
client.post("/api/v1/tasks/", json={"title": "Task 1"})
client.post("/api/v1/tasks/", json={"title": "Task 2"})

```
response = client.get("/api/v1/tasks/")

assert response.status_code == 200
assert len(response.json()) == 2
```

def test_get_task(client: TestClient):
"""Test retrieving a specific task by ID"""
create_response = client.post(
"/api/v1/tasks/",
json={"title": "Test task"}
)
task_id = create_response.json()["id"]

```
response = client.get(f"/api/v1/tasks/{task_id}")

assert response.status_code == 200
assert response.json()["id"] == task_id
assert response.json()["title"] == "Test task"
```

def test_get_task_not_found(client: TestClient):
"""Test retrieving a non-existent task returns 404"""
response = client.get("/api/v1/tasks/999")

```
assert response.status_code == 404
assert "not found" in response.json()["detail"].lower()
```

def test_valid_transition_todo_to_in_progress(client: TestClient):
"""Test valid transition: todo -> in_progress"""
create_response = client.post(
"/api/v1/tasks/",
json={"title": "Task"}
)
task_id = create_response.json()["id"]

```
response = client.patch(
    f"/api/v1/tasks/{task_id}",
    json={"status": TaskStatus.IN_PROGRESS.value}
)

assert response.status_code == 200
assert response.json()["status"] == TaskStatus.IN_PROGRESS.value
```

def test_valid_transition_in_progress_to_done(client: TestClient):
"""Test valid transition: in_progress -> done"""
create_response = client.post(
"/api/v1/tasks/",
json={
"title": "Task",
"status": TaskStatus.IN_PROGRESS.value
}
)
task_id = create_response.json()["id"]

```
response = client.patch(
    f"/api/v1/tasks/{task_id}",
    json={"status": TaskStatus.DONE.value}
)

assert response.status_code == 200
assert response.json()["status"] == TaskStatus.DONE.value
```

def test_invalid_transition_done_to_in_progress(client: TestClient):
"""Test invalid transition: done -> in_progress returns 422"""
create_response = client.post(
"/api/v1/tasks/",
json={
"title": "Task",
"status": TaskStatus.DONE.value
}
)
task_id = create_response.json()["id"]

```
response = client.patch(
    f"/api/v1/tasks/{task_id}",
    json={"status": TaskStatus.IN_PROGRESS.value}
)

assert response.status_code == 422
assert "Invalid transition" in response.json()["detail"]
```

def test_invalid_transition_done_to_todo(client: TestClient):
"""Test invalid transition: done -> todo returns 422"""
create_response = client.post(
"/api/v1/tasks/",
json={
"title": "Task",
"status": TaskStatus.DONE.value
}
)
task_id = create_response.json()["id"]

```
response = client.patch(
    f"/api/v1/tasks/{task_id}",
    json={"status": TaskStatus.TODO.value}
)

assert response.status_code == 422
```

def test_invalid_transition_in_progress_to_todo(client: TestClient):
"""Test invalid transition: in_progress -> todo returns 422"""
create_response = client.post(
"/api/v1/tasks/",
json={
"title": "Task",
"status": TaskStatus.IN_PROGRESS.value
}
)
task_id = create_response.json()["id"]

```
response = client.patch(
    f"/api/v1/tasks/{task_id}",
    json={"status": TaskStatus.TODO.value}
)

assert response.status_code == 422
```

def test_update_preserves_status_when_omitted(client: TestClient):
"""Test that status remains unchanged when not included in update"""
create_response = client.post(
"/api/v1/tasks/",
json={
"title": "Task",
"status": TaskStatus.IN_PROGRESS.value
}
)
task_id = create_response.json()["id"]

```
response = client.patch(
    f"/api/v1/tasks/{task_id}",
    json={"title": "Updated title"}
)

assert response.status_code == 200
assert response.json()["status"] == TaskStatus.IN_PROGRESS.value
assert response.json()["title"] == "Updated title"
```

def test_update_title_and_description(client: TestClient):
"""Test updating title and description without changing status"""
create_response = client.post(
"/api/v1/tasks/",
json={
"title": "Original",
"description": "Original desc"
}
)
task_id = create_response.json()["id"]

```
response = client.patch(
    f"/api/v1/tasks/{task_id}",
    json={
        "title": "Updated",
        "description": "Updated desc"
    }
)

assert response.status_code == 200
assert response.json()["title"] == "Updated"
assert response.json()["description"] == "Updated desc"
```

def test_delete_task(client: TestClient):
"""Test deleting a task"""
create_response = client.post(
"/api/v1/tasks/",
json={"title": "Task to delete"}
)
task_id = create_response.json()["id"]

```
response = client.delete(f"/api/v1/tasks/{task_id}")

assert response.status_code == 200

get_response = client.get(f"/api/v1/tasks/{task_id}")
assert get_response.status_code == 404
```

def test_delete_non_existent_task(client: TestClient):
"""Test deleting a non-existent task returns 404"""
response = client.delete("/api/v1/tasks/999")

```
assert response.status_code == 404
```

def test_create_task_with_due_date(client: TestClient):
"""Test creating a task with a due date"""
response = client.post(
"/api/v1/tasks/",
json={
"title": "Task with due date",
"due_date": "2026-09-10"
}
)

```
assert response.status_code == 200

data = response.json()
assert data["title"] == "Task with due date"
assert data["due_date"] == "2026-09-10"
```

def test_create_task_with_tags(client: TestClient):
"""Test creating a task with tags"""
response = client.post(
"/api/v1/tasks/",
json={
"title": "Tagged task",
"tags": "urgent, work, backend"
}
)

```
assert response.status_code == 200

data = response.json()
assert data["tags"] == "backend, urgent, work"
```

def test_update_task_with_due_date(client: TestClient):
"""Test updating an existing task with a due date"""
create_response = client.post(
"/api/v1/tasks/",
json={"title": "Task"}
)
task_id = create_response.json()["id"]

```
response = client.patch(
    f"/api/v1/tasks/{task_id}",
    json={"due_date": "2026-09-15"}
)

assert response.status_code == 200
assert response.json()["due_date"] == "2026-09-15"
```

def test_update_task_with_tags(client: TestClient):
"""Test updating an existing task with tags"""
create_response = client.post(
"/api/v1/tasks/",
json={"title": "Task"}
)
task_id = create_response.json()["id"]

```
response = client.patch(
    f"/api/v1/tasks/{task_id}",
    json={"tags": "design, urgent"}
)

assert response.status_code == 200
assert response.json()["tags"] == "design, urgent"
```

def test_filter_overdue_tasks(client: TestClient):
"""Test filtering tasks whose due date is before today"""
client.post(
"/api/v1/tasks/",
json={
"title": "Overdue task",
"due_date": "2020-01-01"
}
)

```
client.post(
    "/api/v1/tasks/",
    json={
        "title": "Future task",
        "due_date": "2099-12-31"
    }
)

response = client.get("/api/v1/tasks/?filter=overdue")

assert response.status_code == 200

data = response.json()
titles = [task["title"] for task in data]

assert "Overdue task" in titles
assert "Future task" not in titles
```

def test_filter_tasks_by_tag(client: TestClient):
"""Test filtering tasks by tag"""
client.post(
"/api/v1/tasks/",
json={
"title": "Urgent task",
"tags": "urgent, work"
}
)

```
client.post(
    "/api/v1/tasks/",
    json={
        "title": "Normal task",
        "tags": "work"
    }
)

response = client.get(
    "/api/v1/tasks/?tag=urgent"
)

assert response.status_code == 200

data = response.json()
titles = [task["title"] for task in data]

assert "Urgent task" in titles
assert "Normal task" not in titles
```
def test_create_task_with_due_date(client: TestClient):
"""Test creating a task with a due date"""
response = client.post(
"/api/v1/tasks/",
json={
"title": "Task with due date",
"due_date": "2026-09-10"
}
)

```
assert response.status_code == 200
data = response.json()
assert data["due_date"] == "2026-09-10"
```

def test_create_task_with_tags(client: TestClient):
"""Test creating a task with tags"""
response = client.post(
"/api/v1/tasks/",
json={
"title": "Tagged task",
"tags": "urgent, work, backend"
}
)

```
assert response.status_code == 200
data = response.json()
assert data["tags"] == "backend, urgent, work"
```

def test_update_task_with_due_date(client: TestClient):
"""Test updating a task with a due date"""
create_response = client.post(
"/api/v1/tasks/",
json={"title": "Task"}
)

```
assert create_response.status_code == 200
task_id = create_response.json()["id"]

response = client.patch(
    f"/api/v1/tasks/{task_id}",
    json={"due_date": "2026-09-15"}
)

assert response.status_code == 200
assert response.json()["due_date"] == "2026-09-15"
```

def test_update_task_with_tags(client: TestClient):
"""Test updating a task with tags"""
create_response = client.post(
"/api/v1/tasks/",
json={"title": "Task"}
)

```
assert create_response.status_code == 200
task_id = create_response.json()["id"]

response = client.patch(
    f"/api/v1/tasks/{task_id}",
    json={"tags": "design, urgent"}
)

assert response.status_code == 200
assert response.json()["tags"] == "design, urgent"
```

def test_filter_overdue_tasks(client: TestClient):
"""Test filtering tasks whose due date is before today"""
overdue_response = client.post(
"/api/v1/tasks/",
json={
"title": "Overdue task",
"due_date": "2020-01-01"
}
)

```
future_response = client.post(
    "/api/v1/tasks/",
    json={
        "title": "Future task",
        "due_date": "2099-12-31"
    }
)

assert overdue_response.status_code == 200
assert future_response.status_code == 200

response = client.get("/api/v1/tasks/?filter=overdue")

assert response.status_code == 200

titles = [task["title"] for task in response.json()]

assert "Overdue task" in titles
assert "Future task" not in titles
```

def test_filter_tasks_by_tag(client: TestClient):
"""Test filtering tasks by tag"""
urgent_response = client.post(
"/api/v1/tasks/",
json={
"title": "Urgent task",
"tags": "urgent, work"
}
)

```
normal_response = client.post(
    "/api/v1/tasks/",
    json={
        "title": "Normal task",
        "tags": "work"
    }
)

assert urgent_response.status_code == 200
assert normal_response.status_code == 200

response = client.get("/api/v1/tasks/?tag=urgent")

assert response.status_code == 200

titles = [task["title"] for task in response.json()]

assert "Urgent task" in titles
assert "Normal task" not in titles
```
