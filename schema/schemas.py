from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum, IntEnum
from model.models import PriorityEnum
from datetime import datetime

class SignUpModel(BaseModel):
    name: str = Field(..., example="John Doe", min_length=2, max_length=50, description="Full name of the user")
    email: str = Field(..., example="johndoe123@gmail.com", min_length=5, max_length=80, description="Email address of the user")
    password: str = Field(..., example="strongpassword", min_length=5, max_length=100, description="Password for the user account")

class UserResponse(BaseModel):
    name: str
    email: str
    created_at: datetime
    class Config:
        orm_mode = True

class Settings(BaseModel):
    authjwt_secret_key:str="a9102e7e05287aa2dd1a4333fa7bdad6b5447cef672bc1c9c35d3668f4c02e09"

class LoginModel(BaseModel):
    email: str = Field(..., example="johndoe123@gmail.com", min_length=5, max_length=80, description="Email address of the user")
    password: str = Field(..., example="strongpassword", min_length=5, max_length=100, description="Password for the user account")

class TodoBase(BaseModel):
    description: str = Field(..., example="Morning run at 6 PM", min_length=5, max_length=512, description="Description of the to-do item")
    priority: PriorityEnum = Field(default=PriorityEnum.LOW, example=PriorityEnum.LOW, description="Priority level of the to-do item")
    due_date: Optional[datetime] = Field(None, example="2024-12-31T23:59:59", description="Due date and time for the to-do item")

class TodoModel(TodoBase):
    category_id: int = Field(..., example=1, description="Category ID for the to-do item")

class TodoUpdate(BaseModel):
    description: Optional[str] = Field(None, example="Swimming at 8 AM", min_length=5, max_length=512, description="Description of the to-do item")
    priority: Optional[PriorityEnum] = Field(None, description="Priority level of the to-do item")
    is_completed: Optional[bool] = Field(None, description="Completion status of the to-do item")
    due_date: Optional[datetime] = Field(None, example="2024-12-31T23:59:59", description="Due date and time for the to-do item")
    category_id: Optional[int] = Field(None, example=1, description="Category ID for the to-do item")

class TodoResponse(BaseModel):
    id: int
    created_at: datetime

    todo_name: str
    description: str
    priority: PriorityEnum
    is_completed: bool
    due_date: Optional[datetime]

    class Config:
        orm_mode = True
        use_enum_values = True

class CategoryModel(BaseModel):
    name: str = Field(..., example="Work", min_length=1, max_length=50, description="Name of the category")

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

