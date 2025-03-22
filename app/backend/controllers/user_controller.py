from sqlalchemy.orm import Session
from schemas import user_schema
from services import user_services

def create_user(user: user_schema.UserCreate, db: Session):
    return user_services.create_user(db=db, user=user)

def read_users(skip: int, limit: int, db: Session):
    return user_services.get_users(db=db, skip=skip, limit=limit)

# Add this to app/backend/controllers/user_controller.py
def get_user_by_id(user_id: int, db: Session):
    return user_services.get_user_by_id(db=db, user_id=user_id)