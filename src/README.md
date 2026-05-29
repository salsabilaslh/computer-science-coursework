# MVC User Management System

A User Management System developed using FastAPI, SQLite, and the MVC (Model-View-Controller) Architecture.

This project demonstrates how to separate application logic into Model, View, and Controller layers while implementing CRUD operations and data validation using FastAPI and Pydantic.

---

## Features

- Create User
- Read All Users
- Read User by ID
- Update User Information
- Delete User
- Count Total Users
- Input Validation with Pydantic
- SQLite Database Integration
- Swagger API Documentation
- MVC Architecture

---

## MVC Architecture

| Layer | File | Role |
|---------|---------|---------|
| Model | `users/models.py` | Database operations and data access |
| View | `users/schemas.py` | Data validation and response schemas |
| Controller | `users/router.py` | API request handling |
| Database | `database.py` | Database connection management |
| Application | `main.py` | FastAPI application entry point |

---

## Project Structure

```text
library-system/
│
├── src/
│   ├── database.py
│   ├── main.py
│   │
│   └── users/
│       ├── __init__.py
│       ├── models.py
│       ├── schemas.py
│       └── router.py
│
└── users.db
```

---

## Data Flow

```text
Client Request
       ↓
router.py (Controller)
       ↓
schemas.py (Validation)
       ↓
models.py (Database Logic)
       ↓
SQLite Database
       ↓
JSON Response
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd library-system
```

### Install Dependencies

```bash
pip install fastapi
pip install uvicorn
pip install pydantic
```

### Run Server

```bash
uvicorn src.main:app --reload
```

---

## API Documentation

After running the server:

Swagger UI

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON

```text
http://127.0.0.1:8000/openapi.json
```

---

## API Endpoints

| Method | Endpoint | Description |
|----------|----------|----------|
| GET | `/api/users/` | Get all users |
| POST | `/api/users/` | Create a new user |
| GET | `/api/users/{user_id}` | Get user by ID |
| PUT | `/api/users/{user_id}` | Update user information |
| DELETE | `/api/users/{user_id}` | Delete a user |
| GET | `/api/users/count` | Get total number of users |
| GET | `/` | Health check |

---

## Example Request

### Create User

```json
{
  "name": "Salsabila",
  "email": "salsabila@example.com"
}
```

### Response

```json
{
  "id": 1,
  "name": "Salsabila",
  "email": "salsabila@example.com"
}
```

---

## Technologies Used

- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn

---

## Course Information

Application Programming

Spring 2026

MVC Architecture Practice using FastAPI and SQLite
