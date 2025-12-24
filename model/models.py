from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SqlEnum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum, IntEnum

class PriorityEnum(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(80), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="user")
    todos = relationship("Todo", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"
    
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, default="General")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="category")
    todos = relationship("Todo", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    priority = Column(SqlEnum(PriorityEnum), nullable=False, default=PriorityEnum.LOW)
    description = Column(String(512), nullable=False)
    is_completed = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=True)

    # foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    user = relationship("User", back_populates="todos")
    category = relationship("Category", back_populates="todos")
    
    # property is used to get category name
    @property
    def todo_name(self):
        return self.category.name if self.category else "Others"
