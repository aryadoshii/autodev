from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator, EmailStr
from enum import Enum


class TaskStatus(str, Enum):
    """Enumeration of possible task statuses"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskBase(BaseModel):
    """
    Base schema for Task model containing common fields.
    
    Example:
        >>> task = TaskBase(
        ...     title="Complete project",
        ...     description="Finish the project documentation",
        ...     status=TaskStatus.PENDING
        ... )
        >>> print(task.title)
        'Complete project'
    """
    
    title: str = Field(
        ..., 
        description="Title of the task", 
        min_length=1, 
        max_length=200
    )
    
    description: Optional[str] = Field(
        None,
        description="Detailed description of the task",
        max_length=1000
    )
    
    status: TaskStatus = Field(
        TaskStatus.PENDING,
        description="Current status of the task"
    )
    
    priority: Optional[int] = Field(
        None,
        description="Priority level (1-5, where 5 is highest)",
        ge=1,
        le=5
    )
    
    assignee_email: Optional[EmailStr] = Field(
        None,
        description="Email of the person assigned to this task"
    )
    
    due_date: Optional[datetime] = Field(
        None,
        description="Due date for the task"
    )
    
    class Config:
        """Configuration for the base model"""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class TaskCreate(TaskBase):
    """
    Schema for creating a new task (POST request).
    All fields except optional ones are required.
    
    Example:
        >>> task_create = TaskCreate(
        ...     title="Review pull request",
        ...     description="Review the latest changes in the feature branch",
        ...     status=TaskStatus.IN_PROGRESS,
        ...     priority=4,
        ...     assignee_email="developer@example.com"
        ... )
        >>> print(task_create.title)
        'Review pull request'
    """
    
    # Inherits all fields from TaskBase
    # No additional validation needed for creation
    pass


class TaskUpdate(TaskBase):
    """
    Schema for updating an existing task (PUT request).
    All fields are optional to allow partial updates.
    
    Example:
        >>> task_update = TaskUpdate(
        ...     status=TaskStatus.COMPLETED,
        ...     priority=5
        ... )
        >>> print(task_update.status)
        'completed'
    """
    
    # All fields are optional for update operations
    title: Optional[str] = Field(
        None,
        description="Title of the task",
        min_length=1,
        max_length=200
    )
    
    description: Optional[str] = Field(
        None,
        description="Detailed description of the task",
        max_length=1000
    )
    
    status: Optional[TaskStatus] = Field(
        None,
        description="Current status of the task"
    )
    
    priority: Optional[int] = Field(
        None,
        description="Priority level (1-5, where 5 is highest)",
        ge=1,
        le=5
    )
    
    assignee_email: Optional[EmailStr] = Field(
        None,
        description="Email of the person assigned to this task"
    )
    
    due_date: Optional[datetime] = Field(
        None,
        description="Due date for the task"
    )


class TaskResponse(TaskBase):
    """
    Schema for task response (GET requests including ID and timestamps).
    
    Example:
        >>> task_response = TaskResponse(
        ...     id=1,
        ...     title="Fix bug",
        ...     description="Resolve the login issue",
        ...     status=TaskStatus.COMPLETED,
        ...     created_at=datetime.now(),
        ...     updated_at=datetime.now()
        ... )
        >>> print(task_response.id)
        1
    """
    
    id: int = Field(..., description="Unique identifier for the task")
    
    created_at: datetime = Field(..., description="Timestamp when task was created")
    
    updated_at: datetime = Field(..., description="Timestamp when task was last updated")
    
    class Config:
        """Configuration for the response model"""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }