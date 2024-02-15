import uvicorn
from fastapi import FastAPI

from src.backend.app.addresses.views import router as address_router
from src.backend.app.auth.views import router as auth_router
from src.backend.app.categories.views import router as category_router
from src.backend.app.products.views import router as product_router
from src.backend.app.profiles.views import router as profile_router
from src.backend.app.users.views import router as user_router

app = FastAPI(title="Fast Store")


@app.get("/")
async def root():
    return {"message": "Hello"}


app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")
app.include_router(category_router, prefix="/category")
app.include_router(product_router, prefix="/product")
app.include_router(address_router, prefix="/address")
app.include_router(profile_router, prefix="/profile")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
