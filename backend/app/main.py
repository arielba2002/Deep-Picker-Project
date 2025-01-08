import uvicorn
from fastapi import FastAPI, APIRouter
from app.config import db

app = FastAPI()

def init_app():
    db.init()

    app = FastAPI(
        title= "Deep Picker",
        description= "Login Page",
        version= "1"
    )

    @app.on_event("startup")
    async def starup():
        await db.create_all()
        await generate_role()
    
    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    return app

app = init_app()

def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)