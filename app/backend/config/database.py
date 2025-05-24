# File: ./Deep-Picker-Project/app/backend/config/database.py
from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from functools import lru_cache

# Use environment variables for configuration (consider python-dotenv)
DATABASE_URL = "postgresql://postgres:postgres@db:5432/mydb"

# Asynchronous database connection
database = Database(DATABASE_URL)

# Synchronous SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions
Base = declarative_base()

def init_db():
    """Initialize the database by creating all tables defined in the ORM models."""
    try:
        print("Initializing DB and creating tables...")
        from models import user_model
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as e:
        print("Error during DB initialization:", e)

# Use lru_cache for better performance when getting DB sessions
@lru_cache(maxsize=None)
def get_db_session_maker():
    return SessionLocal

def get_db():
    """Provide a database session for synchronous operations."""
    db = get_db_session_maker()()
    try:
        yield db
    finally:
        db.close()