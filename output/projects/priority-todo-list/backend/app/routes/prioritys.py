from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime

from app.database import get_db
from app.models.priority import Priority
from app.schemas.priority import PriorityCreate, PriorityUpdate, PriorityResponse
from app.auth import get_current_user

router = APIRouter(prefix="/prioritys", tags=["Priority"])

# Pydantic models for request/response validation
class PriorityListResponse(BaseModel):
    items: List[PriorityResponse]
    total: int
    limit: int
    offset: int

class PriorityFilter(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    sort_by: Optional[str] = Field(default="id")
    order: Optional[str] = Field(default="asc")

# Helper function to apply filters and sorting
def apply_filters_and_sorting(query, filters: PriorityFilter):
    if filters.name:
        query = query.filter(Priority.name.ilike(f"%{filters.name}%"))
    
    if filters.color:
        query = query.filter(Priority.color.ilike(f"%{filters.color}%"))
    
    # Apply sorting
    if filters.sort_by:
        if hasattr(Priority, filters.sort_by):
            column = getattr(Priority, filters.sort_by)
            if filters.order == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
    
    return query

@router.get("/", response_model=PriorityListResponse)
async def list_priorities(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0,
    filters: PriorityFilter = Depends()
):
    """
    List all priorities with pagination, filtering, and sorting.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        limit: Number of records to return
        offset: Number of records to skip
        filters: Filter parameters
    
    Returns:
        PriorityListResponse: Paginated list of priorities
    """
    try:
        # Apply filters and sorting
        query = db.query(Priority)
        query = apply_filters_and_sorting(query, filters)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        priorities = query.offset(offset).limit(limit).all()
        
        return PriorityListResponse(
            items=priorities,
            total=total,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving priorities: {str(e)}"
        )

@router.get("/{id}", response_model=PriorityResponse)
async def get_priority(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get a priority by ID.
    
    Args:
        id: Priority ID
        db: Database session
        current_user: Current authenticated user
    
    Returns:
        PriorityResponse: Priority details
    
    Raises:
        HTTPException: 404 if priority not found
    """
    try:
        priority = db.query(Priority).filter(Priority.id == id).first()
        if not priority:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Priority with ID {id} not found"
            )
        return priority
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving priority: {str(e)}"
        )

@router.post("/", response_model=PriorityResponse, status_code=status.HTTP_201_CREATED)
async def create_priority(
    priority_data: PriorityCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new priority.
    
    Args:
        priority_data: Priority creation data
        db: Database session
        current_user: Current authenticated user
    
    Returns:
        PriorityResponse: Created priority details
    """
    try:
        # Check if priority with same name already exists
        existing_priority = db.query(Priority).filter(
            Priority.name == priority_data.name
        ).first()
        
        if existing_priority:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Priority with name '{priority_data.name}' already exists"
            )
        
        # Create new priority
        priority = Priority(**priority_data.dict())
        priority.created_at = datetime.utcnow()
        priority.updated_at = datetime.utcnow()
        
        db.add(priority)
        db.commit()
        db.refresh(priority)
        
        return priority
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating priority: {str(e)}"
        )

@router.put("/{id}", response_model=PriorityResponse)
async def update_priority(
    id: int,
    priority_data: PriorityUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update an existing priority.
    
    Args:
        id: Priority ID
        priority_data: Priority update data
        db: Database session
        current_user: Current authenticated user
    
    Returns:
        PriorityResponse: Updated priority details
    
    Raises:
        HTTPException: 404 if priority not found, 400 if validation fails
    """
    try:
        # Find the priority
        priority = db.query(Priority).filter(Priority.id == id).first()
        if not priority:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Priority with ID {id} not found"
            )
        
        # Check if another priority with same name exists
        if priority_data.name:
            existing_priority = db.query(Priority).filter(
                Priority.name == priority_data.name,
                Priority.id != id
            ).first()
            
            if existing_priority:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Priority with name '{priority_data.name}' already exists"
                )
        
        # Update fields
        update_data = priority_data.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        for key, value in update_data.items():
            setattr(priority, key, value)
        
        db.commit()
        db.refresh(priority)
        
        return priority
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating priority: {str(e)}"
        )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_priority(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete a priority by ID.
    
    Args:
        id: Priority ID
        db: Database session
        current_user: Current authenticated user
    
    Raises:
        HTTPException: 404 if priority not found
    """
    try:
        priority = db.query(Priority).filter(Priority.id == id).first()
        if not priority:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Priority with ID {id} not found"
            )
        
        db.delete(priority)
        db.commit()
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting priority: {str(e)}"
        )