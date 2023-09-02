from fastapi import FastAPI
from .routers import accounts, login, posts

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to theapp API. Go to /docs for the Swagger UI"}


app.include_router(accounts.router)
app.include_router(login.router)
app.include_router(posts.router)