# SQLModel task table definition for SQLite persistence
from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime


class TaskStatus(str, Enum):
    """Allowed task status values per ADR-0001"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskTable(SQLModel, table=True):
    """
    SQLite table model for task persistence.
    table=True tells SQLModel to create a database table for this model.
    """
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)  # Index for faster lookups
    description: str = ""
    status: TaskStatus = Field(default=TaskStatus.TODO)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)