import uvicorn

from fastapi import FastAPI

from auth.routers import router as auth_router
from profiles.routers import router as profile_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth_router)
app.include_router(profile_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=1234,
        reload=True
    )