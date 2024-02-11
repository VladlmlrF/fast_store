import uvicorn
from fastapi import FastAPI

from src.backend.app.auth.views import router as auth_router

app = FastAPI(title="Fast Store")


@app.get("/")
async def root():
    return {"message": "Hello"}


app.include_router(auth_router, prefix="/auth")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
