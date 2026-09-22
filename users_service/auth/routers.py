from fastapi import APIRouter, Response
from auth.auth import Auth
from auth.schemas import SUserRegister, SUserAuth


router = APIRouter(prefix='/auth', tags=['Auth'])
auth_module = Auth()

@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    await auth_module.register(user_data)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth):
    access_token = auth_module.login(response, user_data)
    return {'access_token': await access_token, 'refresh_token': None}


@router.post("/logout/")
async def logout_user(response: Response):
    auth_module.logout(response)
    return {'message': 'Пользователь успешно вышел из системы'}
