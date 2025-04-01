import uvicorn

from fastapi import FastAPI, Response, Request, Depends
from schemas import SUpdateProfile, SUserAuth, SUserRegister
from fastapi.responses import JSONResponse
import httpx
from grpc_client.client import PostClient
from google.protobuf.json_format import MessageToJson

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
    response.set_cookie(key="users_access_token", value=res.json()["access_token"], httponly=True)
    return res.json()

@app.post("/logout")
async def logout(response: Response):
    url = "http://127.0.0.1:1234/auth/logout/"
    res = httpx.post(url, headers={"accept": "application/json"})
    response.delete_cookie(key="users_access_token")
    return res.json()

@app.post("/update_profile")
async def update_profile(request: Request, profile_data: SUpdateProfile):
    url = "http://127.0.0.1:1234/profile/update_profile/"
    print(profile_data.dict())
    res = httpx.post(url, json=profile_data.dict(), headers={"accept": "application/json"}, cookies=request.cookies)
    return res.json()

@app.get("/get_profile")
async def get_profile(request: Request):
    url = "http://127.0.0.1:1234/profile/get_profile/"
    res = httpx.get(url, headers={"accept": "application/json"}, cookies=request.cookies)
    return res.json()


async def get_user_id(request: Request):
    url = "http://127.0.0.1:1234/profile/get_user_id/"
    res = httpx.get(url, headers={"accept": "application/json"}, cookies=request.cookies)
    return int(res)


@app.post("/posts/")
async def create_post(request: Request,
    title: str,
    description: str,
    tags: list[str],
):
    creator_id = get_user_id(request)
    grpc_client = PostClient()
    try:
        response = await grpc_client.create_post(title, description, creator_id, tags, True)
        return MessageToJson(response)
    except Exception as e:
        raise BaseException(str(e))
    
@app.get("/posts/")
async def get_post(request: Request,
    post_id: int
):
    user_id = get_user_id(request)
    grpc_client = PostClient()
    try:
        response = await grpc_client.get_post(post_id, user_id)
        return MessageToJson(response)
    except Exception as e:
        raise BaseException(str(e))
    
@app.delete("/posts/")
async def delete_post(
    request: Request,
    post_id: int
):
    user_id = get_user_id(request)
    grpc_client = PostClient()
    try:
        await grpc_client.delete_post(post_id)
        return {}
    except Exception as e:
        raise BaseException(str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=1236,
        reload=True
    )
    