import pytest
import pytest_asyncio
import httpx
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings
from app.api.dependencies import get_db


@pytest_asyncio.fixture(scope="function")
async def client():
    """Async HTTP client for testing"""
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def mock_db():
    """Mock database session"""
    db = AsyncMock(spec=AsyncSession)
    yield db


@pytest_asyncio.fixture(scope="function")
def test_user_data():
    """Test user data"""
    return {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    }


@pytest_asyncio.fixture(scope="function")
def test_user():
    """Test user model instance"""
    return User(
        id=1,
        email="test@example.com",
        hashed_password="$2b$12$examplehashedpassword",
        full_name="Test User"
    )


@pytest_asyncio.fixture(scope="function")
def valid_tokens(test_user):
    """Valid access and refresh tokens"""
    access_token = create_access_token(data={"sub": str(test_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(test_user.id)})
    return {"access_token": access_token, "refresh_token": refresh_token}


class TestUserRegistration:
    """Test user registration endpoints"""

    @pytest.mark.asyncio
    async def test_register_success(self, client, mock_db, test_user_data):
        """Test successful user registration"""
        # Mock the database operations
        mock_db.execute.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # Mock get_db dependency
        with patch("app.api.endpoints.auth.get_db", return_value=mock_db):
            response = await client.post("/auth/register", json=test_user_data)
            
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["full_name"] == test_user_data["full_name"]
        assert "id" in data
        assert "hashed_password" not in data

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client, mock_db, test_user_data):
        """Test registration with duplicate email"""
        # Mock database to raise integrity error
        from sqlalchemy.exc import IntegrityError
        mock_db.execute.side_effect = IntegrityError("duplicate key", None, None)
        
        with patch("app.api.endpoints.auth.get_db", return_value=mock_db):
            response = await client.post("/auth/register", json=test_user_data)
            
        assert response.status_code == 400
        data = response.json()
        assert "already exists" in data["detail"]

    @pytest.mark.asyncio
    async def test_register_invalid_data(self, client, mock_db):
        """Test registration with invalid data"""
        invalid_data = {
            "email": "invalid-email",
            "password": "short",
            "full_name": ""
        }
        
        with patch("app.api.endpoints.auth.get_db", return_value=mock_db):
            response = await client.post("/auth/register", json=invalid_data)
            
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


class TestUserLogin:
    """Test user login endpoints"""

    @pytest.mark.asyncio
    async def test_login_success(self, client, mock_db, test_user):
        """Test successful user login"""
        # Mock database to return a user
        mock_db.execute.return_value.fetchone.return_value = test_user
        
        with patch("app.api.endpoints.auth.get_db", return_value=mock_db):
            response = await client.post("/auth/login", data={
                "username": test_user.email,
                "password": "password123"
            })
            
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client, mock_db, test_user):
        """Test login with wrong password"""
        # Mock database to return a user but wrong password
        mock_db.execute.return_value.fetchone.return_value = test_user
        
        with patch("app.api.endpoints.auth.get_db", return_value=mock_db):
            response = await client.post("/auth/login", data={
                "username": test_user.email,
                "password": "wrongpassword"
            })
            
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Incorrect email or password"

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client, mock_db):
        """Test login with non-existent user"""
        # Mock database to return None (no user found)
        mock_db.execute.return_value.fetchone.return_value = None
        
        with patch("app.api.endpoints.auth.get_db", return_value=mock_db):
            response = await client.post("/auth/login", data={
                "username": "nonexistent@example.com",
                "password": "password123"
            })
            
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Incorrect email or password"


class TestTokenRefresh:
    """Test token refresh functionality"""

    @pytest.mark.asyncio
    async def test_refresh_valid_token(self, client, mock_db, valid_tokens):
        """Test refreshing with valid refresh token"""
        # Mock database to verify user exists
        mock_db.execute.return_value.fetchone.return_value = User(
            id=1,
            email="test@example.com",
            hashed_password="$2b$12$examplehashedpassword",
            full_name="Test User"
        )
        
        with patch("app.api.endpoints.auth.get_db", return_value=mock_db):
            response = await client.post("/auth/refresh", 
                                       headers={"Authorization": f"Bearer {valid_tokens['refresh_token']}"})
            
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_refresh_expired_token(self, client, mock_db):
        """Test refreshing with expired refresh token"""
        # Create an expired token
        expired_token = create_refresh_token(data={"sub": "1"}, expires_delta=-1)
        
        with patch("app.api.endpoints.auth.get_db", return_value=mock_db):
            response = await client.post("/auth/refresh", 
                                       headers={"Authorization": f"Bearer {expired_token}"})
            
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Could not validate credentials"

    @pytest.mark.asyncio
    async def test_refresh_invalid_token(self, client, mock_db):
        """Test refreshing with invalid refresh token"""
        with patch("app.api.endpoints.auth.get_db", return_value=mock_db):
            response = await client.post("/auth/refresh", 
                                       headers={"Authorization": "Bearer invalid-token"})
            
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Could not validate credentials"


class TestProtectedEndpoints:
    """Test protected endpoint access"""

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_valid_token(self, client, mock_db, valid_tokens):
        """Test accessing protected endpoint with valid token"""
        # Mock database to verify user exists
        mock_db.execute.return_value.fetchone.return_value = User(
            id=1,
            email="test@example.com",
            hashed_password="$2b$12$examplehashedpassword",
            full_name="Test User"
        )
        
        with patch("app.api.endpoints.users.get_db", return_value=mock_db):
            response = await client.get("/users/me", 
                                      headers={"Authorization": f"Bearer {valid_tokens['access_token']}"})
            
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test User"

    @pytest.mark.asyncio
    async def test_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token"""
        response = await client.get("/users/me")
        
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Not authenticated"

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token"""
        response = await client.get("/users/me", 
                                  headers={"Authorization": "Bearer invalid-token"})
        
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Could not validate credentials"

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_expired_token(self, client, mock_db):
        """Test accessing protected endpoint with expired access token"""
        # Create an expired access token
        expired_token = create_access_token(data={"sub": "1"}, expires_delta=-1)
        
        with patch("app.api.endpoints.users.get_db", return_value=mock_db):
            response = await client.get("/users/me", 
                                      headers={"Authorization": f"Bearer {expired_token}"})
            
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Could not validate credentials"


# Additional edge case tests
class TestEdgeCases:
    """Test edge cases for authentication"""

    @pytest.mark.asyncio
    async def test_register_empty_payload(self, client, mock_db):
        """Test registration with empty payload"""
        with patch("app.api.endpoints.auth.get_db", return_value=mock_db):
            response = await client.post("/auth/register", json={})
            
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_login_empty_payload(self, client, mock_db):
        """Test login with empty payload"""
        with patch("app.api.endpoints.auth.get_db", return_value=mock_db):
            response = await client.post("/auth/login", data={})
            
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_refresh_no_authorization_header(self, client):
        """Test refresh without authorization header"""
        response = await client.post("/auth/refresh")
        
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Not authenticated"

    @pytest.mark.asyncio
    async def test_refresh_malformed_authorization_header(self, client):
        """Test refresh with malformed authorization header"""
        response = await client.post("/auth/refresh", 
                                   headers={"Authorization": "Invalid"})
        
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Could not validate credentials"