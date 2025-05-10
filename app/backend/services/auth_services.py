from sqlalchemy.orm import Session
from schemas import user_schema
from models import user_model
from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm

SECRET_KEY = "supersecretkey"  # In production, use env vars
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def signup(user: user_schema.UserCreate, db: Session):
    existing_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")
    hashed_password = get_password_hash(user.password)
    db_user = user_model.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def signin(form_data: OAuth2PasswordRequestForm, db: Session):
    user = db.query(user_model.User).filter(user_model.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    # Include both name and email in the JWT
    access_token = create_access_token(data={"sub": user.email, "name": user.name})
    return {"access_token": access_token, "token_type": "bearer"}
