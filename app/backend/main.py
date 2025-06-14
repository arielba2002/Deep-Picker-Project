import uvicorn
import os
from fastapi import FastAPI
from config.database import init_db
from fastapi.middleware.cors import CORSMiddleware

# Constants (moved to the top for better maintainability)
PORT = int(os.getenv("PORT", "8888"))
HOST = os.getenv("HOST", "0.0.0.0")
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")

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
print("About to initialize database...")
init_db()
print("Database initialization completed!")

# STEP-BY-STEP ROUTE TESTING - Testing auth_routes first
print("About to import auth_routes...")
try:
    from routes import auth_routes
    print("✅ auth_routes imported successfully!")
    app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])
    print("✅ auth_routes registered successfully!")
except Exception as e:
    print(f"❌ Error with auth_routes: {e}")
    import traceback
    traceback.print_exc()

# Adding user_routes to test
print("About to import user_routes...")
try:
    from routes import user_routes
    print("✅ user_routes imported successfully!")
    app.include_router(user_routes.router, prefix="/api/v1", tags=["users"])
    print("✅ user_routes registered successfully!")
except Exception as e:
    print(f"❌ Error with user_routes: {e}")
    import traceback
    traceback.print_exc()

# Adding player_routes to test (likely contains teams endpoint)
print("About to import player_routes...")
try:
    from routes import player_routes
    print("✅ player_routes imported successfully!")
    app.include_router(player_routes.router, prefix="/api/v1", tags=["players"])
    print("✅ player_routes registered successfully!")
except Exception as e:
    print(f"❌ CRITICAL ERROR with player_routes: {e}")
    print(f"❌ Error type: {type(e).__name__}")
    import traceback
    print("❌ Full traceback:")
    traceback.print_exc()
    print("❌ Continuing without player_routes for now...")

print("Testing with all routes: auth + user + player...")

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

print("FastAPI app configured, about to start server...")

def start():
    """Launched with 'poetry run start' at root level"""
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)

if __name__ == "__main__":
    print(f"Starting uvicorn server on {HOST}:{PORT}")
    uvicorn.run("main:app", host=HOST, port=PORT, reload=False)