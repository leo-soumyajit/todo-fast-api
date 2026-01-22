from pydantic import BaseModel, EmailStr, Field, BeforeValidator
from typing import Optional, Annotated
from datetime import datetime

# --- MAGIC FIX: ObjectId ko String banane ke liye ---
PyObjectId = Annotated[str, BeforeValidator(str)]

# --- User Schemas ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
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
    id: PyObjectId   # <--- FIX: alias="_id" hata diya hai
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        from_attributes = True

# --- Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str