from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi_jwt_auth import AuthJWT
from db.database import get_db
from sqlalchemy.orm import Session
from model.models import User, Category
from schema.schemas import SignUpModel, Settings, UserResponse, LoginModel
from werkzeug.security import generate_password_hash, check_password_hash
from seeder.seeders import CATEGORIES_SEED

user_router = APIRouter()

@user_router.get("/")
async def hello(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user_id = Authorize.get_jwt_subject()
    db_user = db.query(User).filter(User.id == current_user_id).first()
    
    return {"Message": f"Welcome {db_user.name}!"}

@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(user: SignUpModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=generate_password_hash(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # seed default categories for the new user
    for category_data in CATEGORIES_SEED:
        category = db.query(Category).filter_by(name=category_data["name"], user_id=new_user.id).first()
        if not category:
            category = Category(name=category_data["name"], user_id=new_user.id)
            db.add(category)
    db.commit()

    return new_user

@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.id)
        refresh_token = Authorize.create_refresh_token(subject=db_user.id)

        response = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return response
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
@user_router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    
    return {"access_token": new_access_token}


    

