from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from . import crud, models, schemas, database
from .database import Base, engine

# Initialize the FastAPI app
app = FastAPI()

# Create the tables in the database
models.Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@app.get("/test-connection/")
def test_connection(db: Session = Depends(get_db)):
    try:
        # Try executing a simple query to check the connection
        db.execute(text("SELECT 1"))
        return {"message": "Database connection successful"}
    except SQLAlchemyError as e:
        # Handle any database connection error
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
