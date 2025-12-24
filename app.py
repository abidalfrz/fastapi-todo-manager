from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
import uvicorn
from routes.auth_routes import user_router
from routes.todo_routes import todo_router
from routes.categories_routes import categories_router
from model.models import Base
from db.database import engine, SessionLocal
from schema.schemas import Settings
from fastapi_jwt_auth import AuthJWT
from fastapi.openapi.utils import get_openapi
from seeder.seeders import seed_data
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_data(db)
    except Exception as e:
        print(f"Error during seeding data: {e}")
    finally:
        db.close()
    yield
    # Shutdown code (if any)

    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    # Generate schema 
    openapi_schema = get_openapi(
        title="To-Do Management API",
        version="1.0.0",
        description="JWT Authentication with FastAPI",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter your token with the format: Bearer <your_token>"
        }
    }
    
    openapi_schema["security"] = [{"Bearer Auth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@AuthJWT.load_config
def get_config():
    return Settings()

Base.metadata.create_all(bind=engine)
    
app.include_router(user_router, prefix="/auth", tags=["auth"])
app.include_router(todo_router, prefix="/todos", tags=["todos"])
app.include_router(categories_router, prefix="/categories", tags=["categories"])

@app.get("/")
async def greet():
    return {"message": "Welcome to the To-Do Management API!"}

if __name__ == '__main__':
    FILE_NAME = "app"
    FUNCTION_NAME = "app"
    HOST = "127.0.0.1"
    PORT = 8000
    uvicorn.run(f"{FILE_NAME}:{FUNCTION_NAME}", host=HOST, port=PORT, reload=True)

