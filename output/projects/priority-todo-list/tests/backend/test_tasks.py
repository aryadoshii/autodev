import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any

# Assuming these are the models and schemas from your application
# You'll need to adjust imports based on your actual project structure
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.api.v1.endpoints.tasks import (
    create_task, get_tasks, get_task_by_id, 
    update_task, delete_task
)
from app.core.security import verify_password, create_access_token
from app.core.config import settings


@pytest.fixture
def mock_db():
    """Mock database session"""
    return MagicMock(spec=Session)


@pytest.fixture
def valid_task_data():
    """Valid task creation data"""
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending",
        "priority": "medium"
    }


@pytest.fixture
def invalid_task_data():
    """Invalid task creation data"""
    return {
        "title": "",  # Empty title
        "description": "This is a test task",
        "status": "invalid_status",  # Invalid status
        "priority": "high"
    }


@pytest.fixture
def existing_task():
    """Existing task object"""
    return Task(
        id=1,
        title="Existing Task",
        description="An existing task",
        status="pending",
        priority="low",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.fixture
def user_payload():
    """User payload for authentication"""
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }


@pytest.fixture
def auth_headers(user_payload):
    """Authentication headers"""
    token = create_access_token(data={"sub": str(user_payload["id"])})
    return {"Authorization": f"Bearer {token}"}


class TestTaskCRUD:
    
    @pytest.mark.asyncio
    async def test_create_task_success(self, mock_db, valid_task_data, auth_headers):
        """Test successful task creation"""
        # Mock database behavior
        mock_task = Task(**valid_task_data, id=1, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Mock the function call
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            result = await create_task(valid_task_data, mock_db, auth_headers)
            
        assert result.title == valid_task_data["title"]
        assert result.status == valid_task_data["status"]
        assert result.id == 1
    
    @pytest.mark.asyncio
    async def test_create_task_invalid_data(self, mock_db, invalid_task_data, auth_headers):
        """Test task creation with invalid data"""
        # Mock database behavior
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            with pytest.raises(HTTPException) as exc_info:
                await create_task(invalid_task_data, mock_db, auth_headers)
            
        assert exc_info.value.status_code == 422
    
    @pytest.mark.asyncio
    async def test_create_task_unauthorized(self, mock_db, valid_task_data):
        """Test task creation without authorization"""
        with patch('app.api.v1.endpoints.tasks.get_current_user', side_effect=HTTPException(status_code=401)):
            with pytest.raises(HTTPException) as exc_info:
                await create_task(valid_task_data, mock_db, {})
            
        assert exc_info.value.status_code == 401
    
    @pytest.mark.asyncio
    async def test_get_all_tasks_with_pagination(self, mock_db, existing_task):
        """Test getting all tasks with pagination"""
        # Mock database behavior
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = [existing_task]
        mock_db.query.return_value.count.return_value = 1
        
        # Mock the function call
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            result = await get_tasks(mock_db, skip=0, limit=10)
            
        assert len(result) == 1
        assert result[0].title == existing_task.title
    
    @pytest.mark.asyncio
    async def test_get_all_tasks_with_filtering(self, mock_db, existing_task):
        """Test getting all tasks with filtering"""
        # Mock database behavior
        mock_db.query.return_value.filter.return_value.all.return_value = [existing_task]
        
        # Mock the function call
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            result = await get_tasks(mock_db, status="pending")
            
        assert len(result) == 1
        assert result[0].status == "pending"
    
    @pytest.mark.asyncio
    async def test_get_task_by_id_success(self, mock_db, existing_task):
        """Test getting task by ID successfully"""
        # Mock database behavior
        mock_db.query.return_value.filter.return_value.first.return_value = existing_task
        
        # Mock the function call
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            result = await get_task_by_id(1, mock_db)
            
        assert result.id == 1
        assert result.title == existing_task.title
    
    @pytest.mark.asyncio
    async def test_get_task_by_id_not_found(self, mock_db):
        """Test getting non-existent task by ID"""
        # Mock database behavior
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            with pytest.raises(HTTPException) as exc_info:
                await get_task_by_id(999, mock_db)
                
        assert exc_info.value.status_code == 404
    
    @pytest.mark.asyncio
    async def test_update_task_success(self, mock_db, existing_task, valid_task_data):
        """Test updating task successfully"""
        # Mock database behavior
        mock_db.query.return_value.filter.return_value.first.return_value = existing_task
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # Mock the function call
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            result = await update_task(1, valid_task_data, mock_db)
            
        assert result.title == valid_task_data["title"]
        assert result.status == valid_task_data["status"]
    
    @pytest.mark.asyncio
    async def test_update_task_not_found(self, mock_db):
        """Test updating non-existent task"""
        # Mock database behavior
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            with pytest.raises(HTTPException) as exc_info:
                await update_task(999, {"title": "Updated Task"}, mock_db)
                
        assert exc_info.value.status_code == 404
    
    @pytest.mark.asyncio
    async def test_update_task_unauthorized(self, mock_db, existing_task):
        """Test updating task without authorization"""
        # Mock database behavior
        mock_db.query.return_value.filter.return_value.first.return_value = existing_task
        
        with patch('app.api.v1.endpoints.tasks.get_current_user', side_effect=HTTPException(status_code=401)):
            with pytest.raises(HTTPException) as exc_info:
                await update_task(1, {"title": "Updated Task"}, mock_db)
                
        assert exc_info.value.status_code == 401
    
    @pytest.mark.asyncio
    async def test_delete_task_success(self, mock_db, existing_task):
        """Test deleting task successfully"""
        # Mock database behavior
        mock_db.query.return_value.filter.return_value.first.return_value = existing_task
        mock_db.delete.return_value = None
        mock_db.commit.return_value = None
        
        # Mock the function call
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            result = await delete_task(1, mock_db)
            
        assert result.message == "Task deleted successfully"
    
    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, mock_db):
        """Test deleting non-existent task"""
        # Mock database behavior
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            with pytest.raises(HTTPException) as exc_info:
                await delete_task(999, mock_db)
                
        assert exc_info.value.status_code == 404
    
    @pytest.mark.asyncio
    async def test_delete_task_unauthorized(self, mock_db, existing_task):
        """Test deleting task without authorization"""
        # Mock database behavior
        mock_db.query.return_value.filter.return_value.first.return_value = existing_task
        
        with patch('app.api.v1.endpoints.tasks.get_current_user', side_effect=HTTPException(status_code=401)):
            with pytest.raises(HTTPException) as exc_info:
                await delete_task(1, mock_db)
                
        assert exc_info.value.status_code == 401
    
    @pytest.mark.asyncio
    async def test_get_all_tasks_empty_result(self, mock_db):
        """Test getting all tasks when none exist"""
        # Mock database behavior
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = []
        mock_db.query.return_value.count.return_value = 0
        
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            result = await get_tasks(mock_db, skip=0, limit=10)
            
        assert len(result) == 0
    
    @pytest.mark.asyncio
    async def test_create_task_duplicate_title(self, mock_db, valid_task_data):
        """Test creating task with duplicate title"""
        # Mock database behavior - simulate existing task with same title
        mock_existing_task = Task(**valid_task_data, id=2, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        mock_db.query.return_value.filter.return_value.first.return_value = mock_existing_task
        
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            with pytest.raises(HTTPException) as exc_info:
                await create_task(valid_task_data, mock_db, {})
                
        assert exc_info.value.status_code == 400
        assert "already exists" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_update_task_invalid_status(self, mock_db, existing_task):
        """Test updating task with invalid status"""
        # Mock database behavior
        mock_db.query.return_value.filter.return_value.first.return_value = existing_task
        
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            with pytest.raises(HTTPException) as exc_info:
                await update_task(1, {"status": "invalid_status"}, mock_db)
                
        assert exc_info.value.status_code == 422
    
    @pytest.mark.asyncio
    async def test_get_tasks_with_invalid_pagination(self, mock_db):
        """Test getting tasks with invalid pagination parameters"""
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            with pytest.raises(HTTPException) as exc_info:
                await get_tasks(mock_db, skip=-1, limit=-1)
                
        assert exc_info.value.status_code == 422


# Additional edge case tests
class TestTaskEdgeCases:
    
    @pytest.mark.asyncio
    async def test_create_task_with_special_characters(self, mock_db, auth_headers):
        """Test creating task with special characters in title/description"""
        special_data = {
            "title": "Task with !@#$%^&*()_+{}|:<>?[]\\;',./",
            "description": "Description with éñü and 🚀 emojis",
            "status": "pending",
            "priority": "high"
        }
        
        mock_task = Task(**special_data, id=1, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            result = await create_task(special_data, mock_db, auth_headers)
            
        assert result.title == special_data["title"]
        assert result.description == special_data["description"]
    
    @pytest.mark.asyncio
    async def test_update_task_partial_fields(self, mock_db, existing_task):
        """Test updating task with partial fields"""
        # Mock database behavior
        mock_db.query.return_value.filter.return_value.first.return_value = existing_task
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # Only update title field
        update_data = {"title": "Partially Updated Task"}
        
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            result = await update_task(1, update_data, mock_db)
            
        assert result.title == "Partially Updated Task"
        # Other fields should remain unchanged
        assert result.description == existing_task.description
        assert result.status == existing_task.status
    
    @pytest.mark.asyncio
    async def test_get_tasks_with_large_limit(self, mock_db, existing_task):
        """Test getting tasks with large limit parameter"""
        # Mock database behavior
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = [existing_task]
        mock_db.query.return_value.count.return_value = 1
        
        with patch('app.api.v1.endpoints.tasks.get_current_user', return_value={"id": 1}):
            result = await get_tasks(mock_db, skip=0, limit=1000000)
            
        assert len(result) == 1
        assert result[0].id == 1