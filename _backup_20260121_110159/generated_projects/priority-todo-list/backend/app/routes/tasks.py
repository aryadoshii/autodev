from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime

from .database import get_db
from .models import Task
from .auth import get_current_user

# Pydantic models for request/response validation
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Router setup
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_user)]
)

# Helper function to apply filters and sorting
def apply_filters_and_sorting(query, title_filter: Optional[str], 
                             completed_filter: Optional[bool], 
                             sort_by: str, order: str):
    if title_filter:
        query = query.filter(Task.title.contains(title_filter))
    
    if completed_filter is not None:
        query = query.filter(Task.completed == completed_filter)
    
    # Apply sorting
    if hasattr(Task, sort_by):
        if order.lower() == "desc":
            query = query.order_by(getattr(Task, sort_by).desc())
        else:
            query = query.order_by(getattr(Task, sort_by).asc())
    else:
        # Default sorting by created_at descending
        query = query.order_by(Task.created_at.desc())
    
    return query

@router.get("/", response_model=List[TaskResponse])
async def read_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    completed: Optional[bool] = None,
    sort_by: str = "created_at",
    order: str = "desc"
):
    """
    Retrieve tasks with pagination, filtering, and sorting.
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        title: Filter tasks by title (partial match)
        completed: Filter tasks by completion status
        sort_by: Field to sort by (default: created_at)
        order: Sort order (asc or desc, default: desc)
    
    Returns:
        List of TaskResponse objects
    """
    try:
        # Validate limit
        if limit > 1000:
            limit = 1000
        
        # Build base query
        query = db.query(Task)
        
        # Apply filters and sorting
        query = apply_filters_and_sorting(
            query, title, completed, sort_by, order
        )
        
        # Apply pagination
        tasks = query.offset(skip).limit(limit).all()
        
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks"
        )

@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a task by its ID.
    
    Args:
        task_id: The ID of the task to retrieve
        db: Database session
    
    Returns:
        TaskResponse object
    
    Raises:
        HTTPException: 404 if task not found
    """
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
        return task
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task"
        )

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.
    
    Args:
        task: Task data to create
        db: Database session
    
    Returns:
        Created TaskResponse object
    """
    try:
        db_task = Task(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create task"
        )

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int, 
    task_update: TaskUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing task.
    
    Args:
        task_id: The ID of the task to update
        task_update: Updated task data
        db: Database session
    
    Returns:
        Updated TaskResponse object
    
    Raises:
        HTTPException: 404 if task not found, 400 if invalid data
    """
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
        
        # Update only provided fields
        update_data = task_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        
        db.commit()
        db.refresh(db_task)
        return db_task
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update task"
        )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by its ID.
    
    Args:
        task_id: The ID of the task to delete
        db: Database session
    
    Raises:
        HTTPException: 404 if task not found
    """
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
        
        db.delete(db_task)
        db.commit()
        return None
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )