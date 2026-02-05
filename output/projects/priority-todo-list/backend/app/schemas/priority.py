from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator, EmailStr
from enum import Enum


class PriorityEnum(str, Enum):
    """Enumeration of priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class PriorityBase(BaseModel):
    """
    Base schema for Priority model containing common fields.
    
    Example:
        >>> PriorityBase(name="High Priority", description="Critical tasks")
        PriorityBase(name='High Priority', description='Critical tasks')
    """
    name: str = Field(
        ...,
        description="Name of the priority level",
        min_length=1,
        max_length=100
    )
    description: Optional[str] = Field(
        None,
        description="Description of the priority level",
        max_length=500
    )
    level: PriorityEnum = Field(
        ...,
        description="Priority level enumeration"
    )
    is_active: bool = Field(
        True,
        description="Whether the priority is active or not"
    )

    class Config:
        """Pydantic configuration"""
        use_enum_values = True
        orm_mode = True


class PriorityCreate(PriorityBase):
    """
    Schema for creating a new Priority.
    Used for POST requests - no ID field required.
    
    Example:
        >>> PriorityCreate(name="Urgent", description="Immediate action needed", level="URGENT")
        PriorityCreate(name='Urgent', description='Immediate action needed', level='URGENT', is_active=True)
    """
    pass


class PriorityUpdate(BaseModel):
    """
    Schema for updating an existing Priority.
    All fields are optional to allow partial updates.
    
    Example:
        >>> PriorityUpdate(description="Updated description", is_active=False)
        PriorityUpdate(description='Updated description', is_active=False)
    """
    name: Optional[str] = Field(
        None,
        description="Name of the priority level",
        min_length=1,
        max_length=100
    )
    description: Optional[str] = Field(
        None,
        description="Description of the priority level",
        max_length=500
    )
    level: Optional[PriorityEnum] = Field(
        None,
        description="Priority level enumeration"
    )
    is_active: Optional[bool] = Field(
        None,
        description="Whether the priority is active or not"
    )

    @validator('name')
    def validate_name_length(cls, v):
        """Validate that name is not empty when provided"""
        if v is not None and len(v.strip()) == 0:
            raise ValueError("Name cannot be empty")
        return v

    class Config:
        """Pydantic configuration"""
        use_enum_values = True
        orm_mode = True


class PriorityResponse(PriorityBase):
    """
    Schema for Priority response including ID and timestamps.
    Used for GET requests and API responses.
    
    Example:
        >>> PriorityResponse(
        ...     id=1,
        ...     name="High Priority",
        ...     description="Critical tasks",
        ...     level="HIGH",
        ...     is_active=True,
        ...     created_at=datetime.now(),
        ...     updated_at=datetime.now()
        ... )
        PriorityResponse(id=1, name='High Priority', description='Critical tasks', ...)
    """
    id: int = Field(..., description="Unique identifier for the priority")
    created_at: datetime = Field(..., description="Timestamp when the priority was created")
    updated_at: datetime = Field(..., description="Timestamp when the priority was last updated")

    class Config:
        """Pydantic configuration"""
        use_enum_values = True
        orm_mode = True