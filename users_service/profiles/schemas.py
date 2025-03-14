from pydantic import BaseModel, EmailStr, Field

class SUpdateProfile(BaseModel):
    first_name: str = Field(..., description="Имя")
    last_name: str = Field(..., description="Фамилия")
    date_of_birth: str = Field(..., description="Дата рождения")
    phone: str = Field(..., description="Телефон")
    photo_url: str = Field(..., description="Ссылка на фотографию")
    about_me: str = Field(..., description="Описание")
    location: str = Field(..., description="Место жительства")