# File: ./Deep-Picker-Project/app/backend/routes/user_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from ..schemas import user_schema
from ..controllers import user_controller
from ..config.database import get_db
from typing import List

router = APIRouter()

@router.post(
    "/users/", 
    response_model=user_schema.User,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided information"
)
def create_user(
    user: user_schema.UserCreate,
    db: Session = Depends(get_db)
):
    return user_controller.create_user(user, db)

@router.get(
    "/users/", 
    response_model=List[user_schema.User],
    summary="Get users list",
    description="Retrieve a list of users with pagination support"
)
def read_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    return user_controller.read_users(skip, limit, db)

@router.get(
    "/users/{user_id}",
    response_model=user_schema.User,
    summary="Get user by ID",
    description="Retrieve a specific user by their ID"
)
def read_user(
    user_id: int = Path(..., gt=0, description="The ID of the user to retrieve"),
    db: Session = Depends(get_db)
):
    user = user_controller.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user