import uvicorn
from fastapi import FastAPI
from config.database import init_db
from fastapi.middleware.cors import CORSMiddleware

# Constants (moved to the top for better maintainability)
PORT = 8888
HOST = "localhost"
FRONTEND_URL = "http://localhost:3000"

# Initialize the FastAPI app
app = FastAPI(
    title="Deep Picker API",
    description="API for the Deep Picker Project",
    version="0.1.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Change to absolute imports
from routes import user_routes
app.include_router(user_routes.router, prefix="/api/v1", tags=["users"])

from routes import player_routes
app.include_router(player_routes.router, prefix="/api/v1", tags=["players"])

from routes import auth_routes
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])


def start():
    """Launched with 'poetry run start' at root level"""
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)