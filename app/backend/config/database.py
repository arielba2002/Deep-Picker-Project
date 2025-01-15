from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/mydb"

# Database connection (async)
database = Database(DATABASE_URL)

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for declarative models
Base = declarative_base()

def init_db():
    # Create the tables in the database
    from ..models import user_model
    Base.metadata.create_all(bind=engine)

# Function to get a synchronous database session
def get_db():
    db = SessionLocal()  # Opens a synchronous connection
    try:
        yield db  # Allows this db session to be injected in route handlers
    finally:
        db.close()  # Closes the session after the request is processed