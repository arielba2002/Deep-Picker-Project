from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import user_schema
from ..controllers import user_controller
from ..config.database import get_db

router = APIRouter()


@router.post("/users/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(user, db)

@router.get("/users/", response_model=list[user_schema.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return user_controller.read_users(skip, limit, db)