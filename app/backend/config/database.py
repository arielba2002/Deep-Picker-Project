# File: ./Deep-Picker-Project/app/backend/config/database.py
from databases import Database
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from functools import lru_cache
import time
import sys
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Use environment variables for configuration (consider python-dotenv)
DATABASE_URL = "postgresql://postgres:postgres@db:5432/mydb"

# Asynchronous database connection
database = Database(DATABASE_URL)

# Synchronous SQLAlchemy setup
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions
Base = declarative_base()

async def wait_for_db(max_retries=5, retry_interval=5):
    """Wait for database to be ready"""
    retries = 0
    while retries < max_retries:
        try:
            # Try to connect to the database
            async with database:
                await database.execute("SELECT 1")
            logger.info("Database connection successful!")
            return True
        except Exception as e:
            retries += 1
            logger.error(f"Database connection attempt {retries} failed: {str(e)}", exc_info=True)
            if retries < max_retries:
                logger.info(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                logger.error("Max retries reached. Could not connect to database.")
                return False

async def init_db():
    """Initialize the database by creating all tables defined in the ORM models."""
    try:
        logger.info("Waiting for database to be ready...")
        if not await wait_for_db():
            logger.error("Failed to connect to database.")
            raise Exception("Database connection failed")

        logger.info("Initializing DB and creating tables...")
        from models import user_model
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully!")

        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
            tables = [row[0] for row in result]
            logger.info(f"Available tables: {tables}")

    except Exception as e:
        logger.error(f"Error during DB initialization: {str(e)}", exc_info=True)
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