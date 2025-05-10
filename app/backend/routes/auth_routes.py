from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import user_schema
from services import auth_services
from config.database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/signup", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def signup(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return auth_services.signup(user, db)

@router.post("/signin")
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_services.signin(form_data, db)
