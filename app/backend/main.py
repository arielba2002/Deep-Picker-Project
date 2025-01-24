import uvicorn
from fastapi import FastAPI
from .config.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware


# Initialize the FastAPI app
app = FastAPI()

# Allow localhost origin (for development purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins (you can restrict this to specific URLs for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# create tables
from .config.database import init_db
init_db()

# Include the user routes
from .routes import user_routes
app.include_router(user_routes.router)


def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("app.backend.main:app", host="localhost", port=8888, reload=True)