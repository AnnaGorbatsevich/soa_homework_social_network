from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from pydantic import EmailStr
from database.dao import UsersDAO
from fastapi import HTTPException, status, Request, Depends
from jose import JWTError
from config import SECRET_KEY, ALGORITHM
from jose import jwt
from fastapi import Response
from database.dao import UsersDAO, ProfileDAO
from auth.schemas import SUserRegister, SUserAuth


class Auth:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def __verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)


    def __create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=30)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt

    async def __authenticate_user(self, email: EmailStr, password: str):
        user = await UsersDAO.find(email=email)
        if not user or self.__verify_password(plain_password=password, hashed_password=user.password) is False:
            return None
        return user

    def __get_token(request: Request):
        token = request.cookies.get('users_access_token')
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
        return token

    async def get_current_user(token: str = Depends(__get_token)):
        try:
            print("TOKEN", token)
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

        expire = payload.get('exp')
        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
        if (not expire) or (expire_time < datetime.now(timezone.utc)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

        user = await UsersDAO.find_by_id(int(user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

        return user
    
    async def login(self, response: Response, user_data: SUserAuth):
        check = await self.__authenticate_user(email=user_data.email, password=user_data.password)
        if check is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Неверная почта или пароль')
        access_token = self.__create_access_token({"sub": str(check.id)})
        response.set_cookie(key="users_access_token", value=access_token, httponly=True)
        return access_token
    
    async def logout(self, response: Response):
        response.delete_cookie(key="users_access_token")
    
    async def register(self, user_data: SUserRegister):
        user = await UsersDAO.find(email=user_data.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Пользователь уже существует'
            )
        user_dict = user_data.dict()
        user_dict['password'] = self.__get_password_hash(user_data.password)
        await UsersDAO.add(**user_dict)
        user = await UsersDAO.find(email=user_data.email)
        await ProfileDAO.add(user_id = user.id, email = user.email)
        
        