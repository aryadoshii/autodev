import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, CalculationHistory, CurrentInput, Result, Operator, Operand
from database import engine

# Create a test database
SQLALCHEMY_DATABASE_URL = \