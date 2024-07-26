class CreateRepositoryMixin:
    async def create(self, **kwargs):
        return await self.objects.create(self.model, **kwargs)

class ReadRepositoryMixin:
    async def get(self, **kwargs):
        model_instance =  await self.objects.get_or_none(self.model, **kwargs)
        return model_instance if model_instance else 'None'

class DeleteRepositoryMixin:
    async def delete(self, id):
        model_instance = await self.objects.get(self.model, id=id)
        await self.objects.delete(model_instance)
        return model_instance
    
class UpdateRepositoryMixin:
    async def update(self, id, only=None, **kwargs):
            model_instance = await self.objects.get(self.model, id=id)
            for key, value in kwargs.items():
                setattr(model_instance, key, value)
            await self.objects.update(model_instance, only=only)
            return model_instance
