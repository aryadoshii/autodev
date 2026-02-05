from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class CalculationHistory(Base):
    __tablename__ = "calculation_history"
    
    id = Column(Integer, primary_key=True, index=True)
    operand1 = Column(Float, nullable=False)
    operand2 = Column(Float, nullable=False)
    operator = Column(String(10), nullable=False)  # +, -, *, /
    result = Column(Float, nullable=True)
    error_message = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_valid = Column(Boolean, default=True)
    
    # Relationships
    current_input_id = Column(Integer, ForeignKey("current_input.id"))
    current_input = relationship("CurrentInput", back_populates="calculations")

class CurrentInput(Base):
    __tablename__ = "current_input"
    
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String(50), nullable=False)
    is_decimal = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    calculations = relationship("CalculationHistory", back_populates="current_input")

class Result(Base):
    __tablename__ = "result"
    
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    calculation_id = Column(Integer, ForeignKey("calculation_history.id"))
    calculation = relationship("CalculationHistory", back_populates="result")

class Operator(Base):
    __tablename__ = "operator"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, nullable=False)  # +, -, *, /
    description = Column(String(255))
    
    # Relationships
    calculations = relationship("CalculationHistory", back_populates="operator")

class Operand(Base):
    __tablename__ = "operand"
    
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    position = Column(Integer, nullable=False)  # 1 or 2 for first or second operand
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    calculation_id = Column(Integer, ForeignKey("calculation_history.id"))
    calculation = relationship("CalculationHistory", back_populates="operands")