from pydantic import BaseModel, EmailStr, Field

class SUserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., description="Пароль")
    login: str = Field(..., description="Логин")
    
class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., description="Пароль")
