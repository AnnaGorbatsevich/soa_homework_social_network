import uvicorn

from fastapi import FastAPI, Response, Request
from schemas import SUpdateProfile, SUserAuth, SUserRegister
import httpx

app = FastAPI()

@app.post("/register")
async def register(user_data: SUserRegister):
    url = "http://127.0.0.1:1234/auth/register/"
    res = httpx.post(url, json=user_data.dict(), headers={"accept": "application/json"})
    return res.json()

@app.post("/login")
async def login(response: Response, user_data: SUserAuth):
    url = "http://127.0.0.1:1234/auth/login/"
    res = httpx.post(url, json=user_data.dict(), headers={"accept": "application/json"})
    return res.json()

@app.post("/logout")
async def logout(response: Response):
    url = "http://127.0.0.1:1234/auth/logout/"
    res = httpx.post(url, headers={"accept": "application/json"})
    return res.json()

@app.post("/update_profile")
async def update_profile(profile_data: SUpdateProfile):
    url = "http://127.0.0.1:1234/profile/update_profile/"
    res = httpx.post(url, json=profile_data.dict(), headers={"accept": "application/json"})
    return res.json()

@app.get("/get_profile")
async def get_profile():
    url = "http://127.0.0.1:1234/profile/get_profile/"
    res = httpx.get(url, headers={"accept": "application/json"})
    return res.json()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=1235,
        reload=True
    )