# 📝 FastAPI Task Management API

This repository containas a RESTful API for managing to-do tasks using FastAPI. The application allows users to create, read, update, and delete tasks, with JWT-based authentication for secure access.

---

## 🧠 Features

- User Authentication: Secure login and registration using JWT tokens.
- Task Management: CRUD (Create, Read, Update, Delete) operations for to-do tasks.
- Database: Persistent storage using SQLite and SQLAlchemy ORM.
- Modern API: Built with FastAPI for high performance and easy development.
- Category Management: CRUD operations for task categories.
- Input Validation: Data validation using Pydantic models.
- Database Seeding: Initial data population for categories.

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI**
- **FastAPI-JWT-Auth**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**
- **Uvicorn**
- **Werkzeug**

---

## 📁 Project Structure

```
fastapi-todo-manager/
│
├── db/
│   ├── database.py         # Database connection & session handling
│   └── __init__.py
│
├── model/
│   ├── models.py           # SQLAlchemy database models (User, ToDo, Category)
│   └── __init__.py
│
├── routes/
│   ├── auth_routes.py       # Endpoints for Login & Register
│   ├── categories_routes.py # Endpoints for managing Categories
│   ├── todo_routes.py       # Endpoints for CRUD To-Dos
│   └── __init__.py
│
├── schema/
│   ├── schemas.py          # Pydantic models for Request/Response validation
│   └── __init__.py
│
├── seeder/
│   ├── seeders.py          # Script to populate initial data (e.g., Categories)
│   └── __init__.py
│
├── .gitignore
├── app.py                  # Main application entry point & routes
├── README.md
└── requirements.txt        # Python dependencies list
```

---

## 📖 API Endpoints

| Method | Endpoint               | Description                     |
|--------|------------------------|---------------------------------|
| POST   | /auth/register         | Register a new user             |
| POST   | /auth/login            | User login and JWT token issue  |
| POST   | /auth/refresh          | Refresh JWT token               |
| GET    | /todos/mytodos         | Get all tasks for the logged-in user |
| POST   | /todos/create          | Create a new task for the user     |
| PUT    | /todos/update/{id}     | Update a specific task by ID       |
| DELETE | /todos/delete/{id}     | Delete a specific task by ID       |
| GET    | /categories/mycategories          | Get all task categories for the logged-in user |
| POST   | /categories/create     | Create a new task category for the user |
| DELETE | /categories/delete/{id}| Delete a specific category by ID   |

---

## 🚀 How to Run

To run this project on your local machine, follow these steps:

### 1. Clone the Repository

Open your terminal and run the following command:

```bash
git clone https://github.com/abidalfrz/fastapi-todo-manager.git
cd fastapi-todo-manager
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On Linux/macOS
venv\Scripts\activate.bat     # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py # the running command is inside app.py

# The API will be accessible at http://localhost:8000
```

### 5. Access the API

FastAPI provides automatic interactive documentation. Open your browser and navigate to:

1. Swagger UI: `http://localhost:8000/docs` - Test endpoints directly from the browser.
2. ReDoc: `http://localhost:8000/redoc` - Alternative API documentation.

---
