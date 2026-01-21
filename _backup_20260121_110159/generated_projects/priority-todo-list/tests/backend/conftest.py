"""
Pytest configuration file for backend testing.
Contains fixtures for database setup, API testing, and authentication.
"""

import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from typing import Generator, Dict, Any
import os

# Import your application modules here
# from app.main import app
# from app.database import get_db
# from app.models import Base
# from app.schemas import UserCreate
# from app.core.security import create_access_token

# Database configuration for testing
TEST_DATABASE_URL = "sqlite:///:memory:"  # In-memory SQLite database for testing

# Create SQLAlchemy engine and session factory for testing
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_db() -> Generator:
    """
    Create a test database session.
    
    Yields:
        Session: SQLAlchemy session for testing
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(test_db) -> Generator:
    """
    Create an AsyncClient for API testing.
    
    Args:
        test_db: Test database session fixture
        
    Yields:
        AsyncClient: HTTP client for making API requests
    """
    # You would typically use your FastAPI app here
    # from app.main import app
    
    # async def override_get_db():
    #     yield test_db
    
    # app.dependency_overrides[get_db] = override_get_db
    
    # async with AsyncClient(app=app, base_url="http://test") as ac:
    #     yield ac
    
    # For now, we'll return a placeholder - replace with actual implementation
    yield None


@pytest.fixture(scope="function")
def test_user(test_db) -> Dict[str, Any]:
    """
    Create a test user in the database.
    
    Args:
        test_db: Test database session fixture
        
    Returns:
        Dict[str, Any]: Test user data
    """
    # Example implementation - adjust according to your models
    # from app.models import User
    # from app.schemas import UserCreate
    # from app.core.security import get_password_hash
    
    # user_data = UserCreate(
    #     email="test@example.com",
    #     password="password123",
    #     full_name="Test User"
    # )
    
    # hashed_password = get_password_hash(user_data.password)
    # db_user = User(
    #     email=user_data.email,
    #     hashed_password=hashed_password,
    #     full_name=user_data.full_name
    # )
    
    # test_db.add(db_user)
    # test_db.commit()
    # test_db.refresh(db_user)
    
    # return {
    #     "id": db_user.id,
    #     "email": db_user.email,
    #     "full_name": db_user.full_name,
    #     "is_active": db_user.is_active
    # }
    
    # Placeholder return
    return {
        "id": 1,
        "email": "test@example.com",
        "full_name": "Test User",
        "is_active": True
    }


@pytest.fixture(scope="function")
def auth_headers(test_user) -> Dict[str, str]:
    """
    Generate authentication headers with a valid JWT token.
    
    Args:
        test_user: Test user fixture
        
    Returns:
        Dict[str, str]: Authorization headers
    """
    # Example implementation - adjust according to your authentication system
    # from app.core.security import create_access_token
    
    # token = create_access_token(data={"sub": str(test_user["id"])})
    # return {"Authorization": f"Bearer {token}"}
    
    # Placeholder return
    return {"Authorization": "Bearer fake-jwt-token"}


@pytest.fixture(scope="function")
def mock_data() -> Dict[str, Any]:
    """
    Provide sample data for entities used in tests.
    
    Returns:
        Dict[str, Any]: Mock data for testing
    """
    return {
        "users": [
            {
                "id": 1,
                "email": "test1@example.com",
                "full_name": "Test User 1",
                "is_active": True
            },
            {
                "id": 2,
                "email": "test2@example.com",
                "full_name": "Test User 2",
                "is_active": False
            }
        ],
        "products": [
            {
                "id": 1,
                "name": "Test Product 1",
                "price": 10.99,
                "description": "A test product"
            },
            {
                "id": 2,
                "name": "Test Product 2",
                "price": 25.50,
                "description": "Another test product"
            }
        ],
        "orders": [
            {
                "id": 1,
                "user_id": 1,
                "product_id": 1,
                "quantity": 2,
                "total_price": 21.98
            }
        ]
    }


@pytest.fixture(scope="function", autouse=True)
def clear_database(test_db):
    """
    Automatically clear database after each test function.
    
    Args:
        test_db: Test database session fixture
    """
    # Begin a new transaction
    test_db.begin()
    
    yield
    
    # Rollback the transaction to clear changes
    test_db.rollback()
    test_db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Setup test database at session level.
    Creates all tables before running tests.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Cleanup if needed (in-memory database will be cleared automatically)
    pass


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_database():
    """
    Cleanup test database at session end.
    """
    yield
    
    # Close engine connection if needed
    engine.dispose()