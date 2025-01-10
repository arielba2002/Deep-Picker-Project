import uvicorn
from fastapi import FastAPI
from .config.database import Base, engine


# Initialize the FastAPI app
app = FastAPI()

# Create the tables in the database
from .models import user_model
user_model.Base.metadata.create_all(bind=engine)

# Dependency to get the database session
from .config import database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Include the user routes
from .routes import user_routes
app.include_router(user_routes.router)


def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)