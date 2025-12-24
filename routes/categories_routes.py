from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_jwt_auth import AuthJWT
from db.database import get_db
from sqlalchemy.orm import Session
from model.models import Category, Todo
from schema.schemas import CategoryModel, CategoryResponse

categories_router = APIRouter()

@categories_router.get("/mycategories", response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_user_categories(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user_id = Authorize.get_jwt_subject()
    categories = db.query(Category).filter(Category.user_id == current_user_id).all()
    if categories:
        return categories
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No categories found")

@categories_router.post("/create", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user_id = Authorize.get_jwt_subject()
    
    new_category = Category(
        name=category.name,
        user_id=current_user_id
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@categories_router.delete("/delete/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user_id = Authorize.get_jwt_subject()

    category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    todo = db.query(Todo).filter(Todo.category_id == category_id).first()
    if todo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete category with associated To-Do items")
    
    
    db.delete(category)
    db.commit()
    
    return {"message": "Category deleted successfully"}