from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi_jwt_auth import AuthJWT
from db.database import SessionLocal, engine
from sqlalchemy.orm import Session, joinedload
from model.models import Todo
from schema.schemas import TodoModel, TodoResponse, TodoUpdate

todo_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@todo_router.get("/mytodos", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
async def get_user_todos(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user_id = Authorize.get_jwt_subject()
    todos = db.query(Todo).options(joinedload(Todo.category)).filter(Todo.user_id == current_user_id).all()
    
    return todos

@todo_router.post("/create", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user_id = Authorize.get_jwt_subject()
    
    new_todo = Todo(
        description=todo.description,
        priority=todo.priority,
        due_date=todo.due_date,
        category_id=todo.category_id,
        user_id=current_user_id
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@todo_router.put("/update/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def update_todo(todo_id: int, todo_update: TodoUpdate, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user_id = Authorize.get_jwt_subject()
    todo = db.query(Todo).options(joinedload(Todo.category)).filter(Todo.id == todo_id, Todo.user_id == current_user_id).first()    
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="To-Do item not found")
    
    todo.description = todo_update.description if todo_update.description is not None else todo.description
    todo.priority = todo_update.priority if todo_update.priority is not None else todo.priority
    todo.is_completed = todo_update.is_completed if todo_update.is_completed is not None else todo.is_completed
    todo.due_date = todo_update.due_date if todo_update.due_date is not None else todo.due_date
    todo.category_id = todo_update.category_id if todo_update.category_id is not None else todo.category_id

    db.commit()
    db.refresh(todo)
    return todo

@todo_router.delete("/delete/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def delete_todo(todo_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user_id = Authorize.get_jwt_subject()
    todo = db.query(Todo).options(joinedload(Todo.category)).filter(Todo.id == todo_id, Todo.user_id == current_user_id).first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="To-Do item not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "To-Do item deleted successfully"}
