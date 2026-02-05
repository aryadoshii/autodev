import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from main import app, get_db
from database import Base
from models import CalculationHistory, CurrentInput, Result, Operator

# Create a test database
SQLALCHEMY_DATABASE_URL = \