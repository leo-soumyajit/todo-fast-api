from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- User Schemas ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    
# --- Todo Schemas ---
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime

# --- Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str