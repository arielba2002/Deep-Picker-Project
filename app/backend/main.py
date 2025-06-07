import logging
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from config.database import init_db, get_db_session_maker
from sqlalchemy import text
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Get environment variables
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8888"))
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://frontend:3000")

logger.info(f"Starting application with HOST={HOST}, PORT={PORT}, FRONTEND_URL={FRONTEND_URL}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting up application...")
        # Initialize database tables
        logger.info("Creating database tables...")
        init_db()
        logger.info("Database tables created successfully")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}", exc_info=True)
        raise

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        # Test database connection
        db = get_db_session_maker()()
        try:
            db.execute(text("SELECT 1"))
            return {"status": "healthy", "database": "connected"}
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Import routes
try:
    logger.info("Importing routes...")
    from routes import auth_routes, user_routes
    logger.info("Routes imported successfully")
except Exception as e:
    logger.error(f"Error importing routes: {str(e)}", exc_info=True)
    raise

# Include routers
try:
    logger.info("Including routers...")
    app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(user_routes.router, prefix="/api/v1/users", tags=["users"])
    logger.info("Routers included successfully")
except Exception as e:
    logger.error(f"Error including routers: {str(e)}", exc_info=True)
    raise

def start():
    try:
        logger.info(f"Starting uvicorn server on {HOST}:{PORT}")
        uvicorn.run(
            "main:app",
            host=HOST,
            port=PORT,
            reload=False,
            log_level="debug"
        )
    except Exception as e:
        logger.error(f"Error starting uvicorn server: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    start()