# Pydantic schemas for API request validation and response serialization
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    """Task status enum for schema validation"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskCreate(BaseModel):
    """Schema for creating a new task (POST request body)"""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: str = Field(default="", max_length=1000, description="Task description")
    status: Optional[TaskStatus] = Field(default=None, description="Initial task status")


class TaskUpdate(BaseModel):
    """Schema for partial task updates (PATCH/PUT request body)"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = Field(None)


class TaskRead(BaseModel):
    """Schema for API responses when returning task data"""
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Allow creation from SQLModel instances