# Task service layer implementing transition validation per ADR-0001
from sqlmodel import Session, select
from app.models.task import TaskTable, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate
from fastapi import HTTPException


# Transition map per ADR-0001: allowed status transitions
ALLOWED_TRANSITIONS = {
    TaskStatus.TODO: {TaskStatus.TODO, TaskStatus.IN_PROGRESS},
    TaskStatus.IN_PROGRESS: {TaskStatus.IN_PROGRESS, TaskStatus.DONE},
    TaskStatus.DONE: {TaskStatus.DONE},
}


class TaskService:
    """Service layer for task business logic including status transition validation"""
    
    @staticmethod
    def create_task(session: Session, task_create: TaskCreate) -> TaskTable:
        """Create a new task in the database"""
        db_task = TaskTable(
            title=task_create.title,
            description=task_create.description,
            status=task_create.status or TaskStatus.TODO
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    
    @staticmethod
    def get_task(session: Session, task_id: int) -> TaskTable:
        """Retrieve a task by ID, raise 404 if not found"""
        task = session.get(TaskTable, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    
    @staticmethod
    def list_tasks(session: Session) -> list[TaskTable]:
        """Retrieve all tasks from the database"""
        statement = select(TaskTable)
        return session.exec(statement).all()
    
    @staticmethod
    def validate_transition(current_status: TaskStatus, new_status: TaskStatus) -> bool:
        """
        Validate if a status transition is allowed per ADR-0001.
        Returns True if valid, raises HTTPException if invalid.
        """
        if new_status not in ALLOWED_TRANSITIONS[current_status]:
            allowed = ", ".join([s.value for s in ALLOWED_TRANSITIONS[current_status]])
            raise HTTPException(
                status_code=422,
                detail=f"Invalid transition from '{current_status.value}' to '{new_status.value}'. Allowed transitions: {allowed}"
            )
        return True
    
    @staticmethod
    def update_task(session: Session, task_id: int, task_update: TaskUpdate) -> TaskTable:
        """
        Update a task with validation. If status transition is invalid,
        raise 422 error before applying any changes (atomic validation).
        """
        db_task = TaskService.get_task(session, task_id)
        
        # Validate status transition first (before any mutations)
        if task_update.status and task_update.status != db_task.status:
            TaskService.validate_transition(db_task.status, task_update.status)
        
        # Apply updates after validation succeeds
        if task_update.title is not None:
            db_task.title = task_update.title
        if task_update.description is not None:
            db_task.description = task_update.description
        if task_update.status is not None:
            db_task.status = task_update.status
        
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    
    @staticmethod
    def delete_task(session: Session, task_id: int) -> None:
        """Delete a task from the database"""
        db_task = TaskService.get_task(session, task_id)
        session.delete(db_task)
        session.commit()