from database.models import Device
import peewee_async

class DeviceRepository:
    def __init__(self, database):
        
        """
        Enabling async peewee Manager
        """
        self.database = database
        self.objects = peewee_async.Manager(database)
        database.set_allow_sync(False)

    async def create(self, **kwargs):
        print('here')
        device = await self.objects.create(Device, **kwargs)
        await self.database.close()
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
