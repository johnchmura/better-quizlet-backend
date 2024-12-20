from fastapi import FastAPI
from .routes import user_routes
from .middleware import auth

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}