"""
Database and authentication dependencies for FastAPI application.

This module provides reusable FastAPI dependencies for database sessions,
JWT token validation, and user authentication/authorization checks.
"""

from typing import Generator, Optional
from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from passlib.context import CryptContext
import os

from .database import SessionLocal
from .models import User
from .schemas import TokenData

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency.
    
    Provides a database session for each request and ensures proper cleanup.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example: