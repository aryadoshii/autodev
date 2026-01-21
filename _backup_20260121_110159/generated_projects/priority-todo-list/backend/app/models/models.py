from sqlalchemy import Column, String, UUID, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

from sqlalchemy import Column, String, UUID, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Priority(Base):
    """
    Represents a priority level for tasks.
    
    Attributes:
        level (UUID): Unique identifier for the priority level.
        label (str): Human-readable label for the priority (e.g., 'High', 'Medium').
        color_code (str): Hex color code representing the priority visually.
        created_at (datetime): Timestamp when the priority was created.
        updated_at (datetime): Timestamp when the priority was last updated.
    """
    __tablename__ = 'priorities'

    level = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String(50), nullable=False, unique=True)
    color_code = Column(String(7), nullable=False)  # Hex color code
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    tasks = relationship("Task", back_populates="priority")

from sqlalchemy import Column, String, UUID, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
import uuid

class Task(Base):
    """
    Represents a task in the todo list.
    
    Attributes:
        id (UUID): Unique identifier for the task.
        title (str): Title of the task.
        description (str): Detailed description of the task.
        due_date (datetime): Deadline for completing the task.
        is_completed (bool): Indicates if the task is completed.
        priority_level (UUID): Foreign key referencing the priority level.
        created_at (datetime): Timestamp when the task was created.
        updated_at (datetime): Timestamp when the task was last updated.
    """
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)
    is_completed = Column(Boolean, default=False)
    priority_level = Column(UUID(as_uuid=True), ForeignKey('priorities.level'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    priority = relationship("Priority", back_populates="tasks")

