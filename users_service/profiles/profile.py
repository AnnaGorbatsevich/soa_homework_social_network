from database.dao import ProfileDAO

class Profile:
    def __init__(self):
        pass
    
    def update(self, profile_data, user_id):
        pass
    
    async def get(self, user_id):
        return await ProfileDAO.find(user_id = int(user_id))
        