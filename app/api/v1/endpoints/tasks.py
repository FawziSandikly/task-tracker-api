# Task endpoints implementing CRUD operations per ADR-0001
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.models.task import TaskTable
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead)
def create_task(
    task_create: TaskCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new task.
    Request body: title (required), description (optional), status (optional, defaults to 'todo')
    Returns: Created task with ID and timestamps
    """
    return TaskService.create_task(session, task_create)


@router.get("/", response_model=list[TaskRead])
def list_tasks(session: Session = Depends(get_session)):
    """
    List all tasks.
    Returns: Array of all tasks in the database
    """
    return TaskService.list_tasks(session)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)):
    """
    Get a specific task by ID.
    Returns: Task with matching ID or 404 if not found
    """
    return TaskService.get_task(session, task_id)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
):
    """
    Partially update a task. Only provided fields are updated.
    Status transitions are validated per ADR-0001 transition rules.
    Invalid transitions return 422 Unprocessable Entity and leave task unchanged.
    """
    return TaskService.update_task(session, task_id, task_update)


@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    """
    Delete a task by ID.
    Returns: 204 No Content on success
    """
    TaskService.delete_task(session, task_id)
    return {"message": "Task deleted successfully"}