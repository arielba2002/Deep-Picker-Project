from ..schemas import user_schema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from ..models import user_model
from fastapi import HTTPException, status

def create_user(db: Session, user: user_schema.UserCreate):
    """
    Create a new user in the database.
    
    Args:
        db: Database session
        user: User data
        
    Returns:
        Created user object
        
    Raises:
        HTTPException: If a user with the same email already exists
                      or other database errors occur
    """
    try:
        # Check if user with this email already exists
        existing_user = db.query(user_model.User).filter(
            user_model.User.email == user.email
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
            
        # Create new user
        db_user = user_model.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
    Get a list of users with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of users
    """
    return db.query(user_model.User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    """
    Get a user by ID.
    
    Args:
        db: Database session
        user_id: ID of the user to retrieve
        
    Returns:
        User object if found
        
    Raises:
        HTTPException: If user not found
    """
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user