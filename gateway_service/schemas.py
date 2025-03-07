from pydantic import BaseModel, EmailStr, Field
from datetime import date as dt

class SUserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., description="Пароль")
    login: str = Field(..., description="Логин")
    
class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., description="Пароль")

class SUpdateProfile(BaseModel):
    first_name: str = Field(..., description="Имя")
    last_name: str = Field(..., description="Фамилия")
    date_of_birth: dt = Field(..., description="Дата рождения")
    phone: str = Field(..., description="Телефон")
    photo_url: str = Field(..., description="Ссылка на фотографию")
    about_me: str = Field(..., description="Описание")
    location: str = Field(..., description="Место жительства")
