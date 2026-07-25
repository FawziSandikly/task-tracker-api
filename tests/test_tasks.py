# Tests for task CRUD endpoints and status transition validation
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.schemas.task import TaskStatus


def test_create_task(client: TestClient):
    """Test creating a new task with default status"""
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "Buy groceries", "description": "Milk, eggs, bread"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["status"] == TaskStatus.TODO.value
    assert data["id"] is not None


def test_list_tasks_empty(client: TestClient):
    """Test listing tasks when database is empty"""
    response = client.get("/api/v1/tasks/")
    
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_with_data(client: TestClient):
    """Test listing tasks after creating multiple tasks"""
    # Create two tasks
    client.post("/api/v1/tasks/", json={"title": "Task 1"})
    client.post("/api/v1/tasks/", json={"title": "Task 2"})
    
    response = client.get("/api/v1/tasks/")
    
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task(client: TestClient):
    """Test retrieving a specific task by ID"""
    create_response = client.post("/api/v1/tasks/", json={"title": "Test task"})
    task_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/tasks/{task_id}")
    
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Test task"


def test_get_task_not_found(client: TestClient):
    """Test retrieving a non-existent task returns 404"""
    response = client.get("/api/v1/tasks/999")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_valid_transition_todo_to_in_progress(client: TestClient):
    """Test valid transition: todo -> in_progress"""
    create_response = client.post("/api/v1/tasks/", json={"title": "Task"})
    task_id = create_response.json()["id"]
    
    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"status": TaskStatus.IN_PROGRESS.value}
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == TaskStatus.IN_PROGRESS.value


def test_valid_transition_in_progress_to_done(client: TestClient):
    """Test valid transition: in_progress -> done"""
    create_response = client.post(
        "/api/v1/tasks/",
        json={"title": "Task", "status": TaskStatus.IN_PROGRESS.value}
    )
    task_id = create_response.json()["id"]
    
    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"status": TaskStatus.DONE.value}
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == TaskStatus.DONE.value


def test_invalid_transition_done_to_in_progress(client: TestClient):
    """Test invalid transition: done -> in_progress returns 422"""
    create_response = client.post(
        "/api/v1/tasks/",
        json={"title": "Task", "status": TaskStatus.DONE.value}
    )
    task_id = create_response.json()["id"]
    
    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"status": TaskStatus.IN_PROGRESS.value}
    )
    
    assert response.status_code == 422
    assert "Invalid transition" in response.json()["detail"]


def test_invalid_transition_done_to_todo(client: TestClient):
    """Test invalid transition: done -> todo returns 422"""
    create_response = client.post(
        "/api/v1/tasks/",
        json={"title": "Task", "status": TaskStatus.DONE.value}
    )
    task_id = create_response.json()["id"]
    
    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"status": TaskStatus.TODO.value}
    )
    
    assert response.status_code == 422


def test_invalid_transition_in_progress_to_todo(client: TestClient):
    """Test invalid transition: in_progress -> todo returns 422"""
    create_response = client.post(
        "/api/v1/tasks/",
        json={"title": "Task", "status": TaskStatus.IN_PROGRESS.value}
    )
    task_id = create_response.json()["id"]
    
    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"status": TaskStatus.TODO.value}
    )
    
    assert response.status_code == 422


def test_update_preserves_status_when_omitted(client: TestClient):
    """Test that status remains unchanged when not included in update"""
    create_response = client.post(
        "/api/v1/tasks/",
        json={"title": "Task", "status": TaskStatus.IN_PROGRESS.value}
    )
    task_id = create_response.json()["id"]
    
    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Updated title"}
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == TaskStatus.IN_PROGRESS.value
    assert response.json()["title"] == "Updated title"


def test_update_title_and_description(client: TestClient):
    """Test updating title and description without changing status"""
    create_response = client.post(
        "/api/v1/tasks/",
        json={"title": "Original", "description": "Original desc"}
    )
    task_id = create_response.json()["id"]
    
    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Updated", "description": "Updated desc"}
    )
    
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"
    assert response.json()["description"] == "Updated desc"


def test_delete_task(client: TestClient):
    """Test deleting a task"""
    create_response = client.post("/api/v1/tasks/", json={"title": "Task to delete"})
    task_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/tasks/{task_id}")
    
    assert response.status_code == 200
    
    # Verify task is actually deleted
    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_non_existent_task(client: TestClient):
    """Test deleting a non-existent task returns 404"""
    response = client.delete("/api/v1/tasks/999")
    
    assert response.status_code == 404