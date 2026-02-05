from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
from database import engine, get_db
from pydantic import BaseModel
from datetime import datetime

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=\