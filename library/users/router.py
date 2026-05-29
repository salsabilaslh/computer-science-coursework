from fastapi import APIRouter, HTTPException
from . import models, schemas

router = APIRouter()

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate):
    """API Endpoint to register a new user."""
    try:
        user_id = models.insert_user(user.name, user.email)
        return schemas.UserResponse(id=user_id, name=user.name, email=user.email)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Email already exists or database error.")

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int):
    """API Endpoint to fetch a specific user by ID."""
    user = models.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserResponse(id=user["id"], name=user["name"], email=user["email"])

@router.get("/users/", response_model=list[schemas.UserResponse])
def read_all_users():
    """API Endpoint to fetch all registered users."""
    users = models.get_all_users()
    return [schemas.UserResponse(id=u["id"], name=u["name"], email=u["email"]) for u in users]