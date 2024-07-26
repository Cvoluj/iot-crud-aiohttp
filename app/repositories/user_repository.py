from database.models import ApiUser
from database import get_async_database

class UserRepository:
    def __init__(self):
        self.objects = get_async_database()

    async def create(self, **kwargs):
        user = await self.objects.create(ApiUser, **kwargs)
        return user

    async def get(self, **kwargs):
        user = await self.objects.get_or_none(ApiUser, **kwargs)
        return user if user else 'None'

    async def update(self, user_id, **kwargs):
        user = await self.objects.get(ApiUser, id=user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        await self.objects.update(user, only=['name', 'password'])
        return user

    async def delete(self, user_id):
        user = await self.objects.get(ApiUser, id=user_id)
        await self.objects.delete(user)
        return user
