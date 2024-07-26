from repositories import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, **kwargs):
        return await self.user_repository.create(**kwargs)

    async def get_user(self, **kwargs):
        """
        Use dict for object, f.e. email=email for search user by email
        use with caution, because if field can repeats you can get wrong user 
        """
        return await self.user_repository.get(**kwargs)

    async def update_user(self, user_id, **kwargs):
        return await self.user_repository.update(user_id, **kwargs)

    async def delete_user(self, user_id):
        return await self.user_repository.delete(user_id)