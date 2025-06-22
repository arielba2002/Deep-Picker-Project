import uvicorn
import os
from fastapi import FastAPI
from config.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_routes, user_routes, player_routes

# Initialize the FastAPI app
app = FastAPI(
    title="Deep Picker API",
    description="API for the Deep Picker Project",
    version="0.1.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user_routes.router, prefix="/api/v1", tags=["users"])
app.include_router(player_routes.router, prefix="/api/v1", tags=["players"])

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

def start():
    """Launched with 'poetry run start' at root level"""
    port = int(os.getenv("PORT", 8888))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8888))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)