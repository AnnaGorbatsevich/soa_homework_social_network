from fastapi import APIRouter, Depends
from profiles.profile import Profile
from database.models import User
from auth.auth import Auth
from profiles.schemas import SUpdateProfile


router = APIRouter(prefix='/profile', tags=['Profile'])
profile_module = Profile()

@router.get("/get_profile/")
async def get_profile(user_data: User = Depends(Auth.get_current_user)):
    profile = await profile_module.get(user_data.id)
    return profile

@router.post("/update_profile/")
async def update_profile(profile_data: SUpdateProfile, user_data: User = Depends(Auth.get_current_user)):
    profile_module.update(profile_data, user_data)
    return {'message': ' Информация о профиле текущего юзера TODO'}

@router.get("/get_user_id/")
async def get_profile(user_id: int = Depends(Auth.get_user_id)):
    return str(user_id)
