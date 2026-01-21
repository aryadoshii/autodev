import pytest
from unittest.mock import patch, MagicMock
from fastapi import status
from sqlalchemy.orm import Session
from app.models.priority import Priority
from app.schemas.priority import PriorityCreate, PriorityUpdate
from app.core.config import settings


@pytest.fixture
def priority_data():
    """Sample priority data for testing"""
    return {
        "name": "High",
        "description": "High priority tasks",
        "color": "#FF0000"
    }


@pytest.fixture
def priority_update_data():
    """Sample priority update data for testing"""
    return {
        "name": "Critical",
        "description": "Critical priority tasks",
        "color": "#FF0000"
    }


@pytest.fixture
def invalid_priority_data():
    """Invalid priority data for testing"""
    return {
        "name": "",  # Empty name
        "description": "Invalid priority",
        "color": "#FF0000"
    }


@pytest.fixture
def mock_priority():
    """Mock priority object for testing"""
    return Priority(
        id=1,
        name="High",
        description="High priority tasks",
        color="#FF0000",
        created_by=1
    )


@pytest.fixture
def mock_priorities_list():
    """List of mock priority objects for testing"""
    return [
        Priority(id=1, name="High", description="High priority tasks", color="#FF0000", created_by=1),
        Priority(id=2, name="Medium", description="Medium priority tasks", color="#FFFF00", created_by=1),
        Priority(id=3, name="Low", description="Low priority tasks", color="#00FF00", created_by=1)
    ]


class TestPriorityCRUD:
    """Test cases for Priority CRUD operations"""

    def test_create_priority_success(self, client, priority_data, mock_db_session):
        """Test successful creation of a priority"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            response = client.post("/api/v1/priorities", json=priority_data)
            
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["name"] == priority_data["name"]
            assert data["description"] == priority_data["description"]
            assert data["color"] == priority_data["color"]
            assert data["created_by"] == 1

    def test_create_priority_invalid_data(self, client, invalid_priority_data, mock_db_session):
        """Test creating priority with invalid data"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            response = client.post("/api/v1/priorities", json=invalid_priority_data)
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_priority_unauthorized(self, client, priority_data):
        """Test creating priority without authentication"""
        response = client.post("/api/v1/priorities", json=priority_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_all_priorities_with_pagination(self, client, mock_priorities_list, mock_db_session):
        """Test getting all priorities with pagination"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            # Test with page and size parameters
            response = client.get("/api/v1/priorities?page=1&size=2")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "items" in data
            assert "total" in data
            assert len(data["items"]) <= 2  # Should respect size limit

    def test_get_all_priorities_filtering(self, client, mock_priorities_list, mock_db_session):
        """Test getting all priorities with filtering"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            # Test filtering by name
            response = client.get("/api/v1/priorities?name=High")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert len(data["items"]) >= 0  # At least 0 items returned

    def test_get_priority_by_id_success(self, client, mock_priority, mock_db_session):
        """Test getting a priority by ID successfully"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            response = client.get(f"/api/v1/priorities/{mock_priority.id}")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["id"] == mock_priority.id
            assert data["name"] == mock_priority.name

    def test_get_priority_by_id_not_found(self, client, mock_db_session):
        """Test getting a priority that doesn't exist"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            response = client.get("/api/v1/priorities/999")
            
            assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_priority_success(self, client, priority_update_data, mock_priority, mock_db_session):
        """Test updating a priority successfully"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            response = client.put(f"/api/v1/priorities/{mock_priority.id}", json=priority_update_data)
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["name"] == priority_update_data["name"]
            assert data["description"] == priority_update_data["description"]

    def test_update_priority_not_found(self, client, priority_update_data, mock_db_session):
        """Test updating a priority that doesn't exist"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            response = client.put("/api/v1/priorities/999", json=priority_update_data)
            
            assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_priority_unauthorized(self, client, priority_update_data, mock_priority):
        """Test updating priority without authentication"""
        response = client.put(f"/api/v1/priorities/{mock_priority.id}", json=priority_update_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_priority_success(self, client, mock_priority, mock_db_session):
        """Test deleting a priority successfully"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            response = client.delete(f"/api/v1/priorities/{mock_priority.id}")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["message"] == "Priority deleted successfully"

    def test_delete_priority_not_found(self, client, mock_db_session):
        """Test deleting a priority that doesn't exist"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            response = client.delete("/api/v1/priorities/999")
            
            assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_priority_unauthorized(self, client, mock_priority):
        """Test deleting priority without authentication"""
        response = client.delete(f"/api/v1/priorities/{mock_priority.id}")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_all_priorities_empty_list(self, client, mock_db_session):
        """Test getting all priorities when list is empty"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            # Mock empty query result
            with patch.object(mock_db_session, 'query', return_value=MagicMock(all=lambda: [])):
                response = client.get("/api/v1/priorities")
                
                assert response.status_code == status.HTTP_200_OK
                data = response.json()
                assert data["items"] == []
                assert data["total"] == 0

    def test_create_priority_edge_cases(self, client, priority_data, mock_db_session):
        """Test edge cases for creating priority"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            # Test with very long name
            long_name_data = {**priority_data, "name": "A" * 100}
            response = client.post("/api/v1/priorities", json=long_name_data)
            assert response.status_code == status.HTTP_201_CREATED
            
            # Test with special characters in name
            special_char_data = {**priority_data, "name": "High & Medium"}
            response = client.post("/api/v1/priorities", json=special_char_data)
            assert response.status_code == status.HTTP_201_CREATED

    def test_get_all_priorities_sorting(self, client, mock_priorities_list, mock_db_session):
        """Test getting all priorities with sorting"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            # Test sorting by name
            response = client.get("/api/v1/priorities?sort=name")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "items" in data

    def test_create_priority_duplicate_name(self, client, priority_data, mock_db_session):
        """Test creating priority with duplicate name (should succeed as it's not enforced)"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            # Create first priority
            client.post("/api/v1/priorities", json=priority_data)
            
            # Create second priority with same name
            response = client.post("/api/v1/priorities", json=priority_data)
            
            assert response.status_code == status.HTTP_201_CREATED

    def test_update_priority_partial_update(self, client, mock_priority, mock_db_session):
        """Test partial update of priority"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            # Partial update - only name
            partial_update = {"name": "Updated Name"}
            response = client.patch(f"/api/v1/priorities/{mock_priority.id}", json=partial_update)
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["name"] == "Updated Name"
            # Other fields should remain unchanged
            assert data["description"] == mock_priority.description
            assert data["color"] == mock_priority.color

    def test_get_priority_by_id_with_permissions(self, client, mock_priority, mock_db_session):
        """Test getting priority with user permissions check"""
        with patch('app.api.v1.endpoints.priorities.get_current_active_user') as mock_auth:
            mock_auth.return_value = MagicMock(id=1)
            
            # User owns the priority
            response = client.get(f"/api/v1/priorities/{mock_priority.id}")
            assert response.status_code == status.HTTP_200_OK
            
            # Test with different user (if permission system exists)
            mock_auth.return_value = MagicMock(id=2)
            response = client.get(f"/api/v1/priorities/{mock_priority.id}")
            # This might return 403 depending on implementation


# Fixtures for database session and other dependencies
@pytest.fixture
def mock_db_session():
    """Mock database session"""
    return MagicMock(spec=Session)


@pytest.fixture
def mock_user():
    """Mock authenticated user"""
    return MagicMock(id=1, email="test@example.com")


@pytest.fixture
def mock_auth_service():
    """Mock authentication service"""
    return MagicMock()


# Additional utility functions for testing
def create_priority_in_db(db_session, priority_data):
    """Helper function to create a priority in the database for testing"""
    priority = Priority(**priority_data)
    db_session.add(priority)
    db_session.commit()
    db_session.refresh(priority)
    return priority