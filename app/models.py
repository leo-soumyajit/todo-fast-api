from beanie import Document, Link
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class User(Document):
    username: str = Field(..., unique=True) # Unique username
    email: EmailStr = Field(..., unique=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users" # Collection name in MongoDB

class Todo(Document):
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Ye link batayega ki ye Todo kis user ka hai
    owner: Link[User] 

    class Settings:
        name = "todos"