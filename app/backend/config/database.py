# File: ./Deep-Picker-Project/app/backend/config/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from functools import lru_cache

# Use environment variables for configuration (consider python-dotenv)
DATABASE_URL = "postgresql://postgres:postgres@db.deep.svc.cluster.local:5432/mydb"

# Synchronous SQLAlchemy setup
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
    echo=False           # Set to True for SQL debugging
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions
Base = declarative_base()

def init_db():
    """Initialize the database by creating all tables defined in the ORM models."""
    import time
    max_retries = 5
    retry_delay = 3
    
    for attempt in range(max_retries):
        try:
            print(f"Initializing DB and creating tables... (attempt {attempt + 1}/{max_retries})")
            print(f"Connecting to: {DATABASE_URL}")
            from models import user_model
            Base.metadata.create_all(bind=engine)
            print("Tables created successfully!")
            return
        except Exception as e:
            print(f"Error during DB initialization (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Database initialization failed.")
                raise

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