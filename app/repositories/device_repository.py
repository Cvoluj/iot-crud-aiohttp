from database.models import Device
from database import get_async_database

class DeviceRepository:
    def __init__(self):
        self.objects = get_async_database()

    async def create(self, **kwargs):
        device = await self.objects.create(Device, **kwargs)
        return device

    async def get(self, device_id):
        return await self.objects.get(Device, id=device_id)

    async def update(self, device_id, **kwargs):
        device = await self.objects.get(Device, id=device_id)
        for key, value in kwargs.items():
            setattr(device, key, value)
        await self.objects.update(device)
        return device

    async def delete(self, device_id):
        device = await self.objects.get(Device, id=device_id)
        await self.objects.delete(device)
        return device
