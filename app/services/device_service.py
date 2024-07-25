from repositories.device_repository import DeviceRepository

class DeviceService:
    def __init__(self, device_repository: DeviceRepository):
        self.device_repository = device_repository

    async def create_device(self, **kwargs):
        return await self.device_repository.create(**kwargs)

    async def get_device(self, device_id):
        return await self.device_repository.get(device_id)

    async def update_device(self, device_id, **kwargs):
        return await self.device_repository.update(device_id, **kwargs)

    async def delete_device(self, device_id):
        return await self.device_repository.delete(device_id)
