from ..schemas import user_schema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import user_model

# Create a user
def create_user(db: Session, user: user_schema.UserCreate):
    try:
        db_user = user_model.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception("Error creating user: " + str(e))

# Get all users
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(user_model.User).offset(skip).limit(limit).all()
