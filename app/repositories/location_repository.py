from peewee import DoesNotExist

from database.models import Location
from database import get_async_database

class LocationRepository:
    def __init__(self):
        self.objects = get_async_database()

    async def create(self, **kwargs):
        return await self.objects.create(Location, **kwargs)

    async def get(self, location_id):
        try:
            return await self.objects.get(Location, id=location_id)
        except DoesNotExist:
            return None

    async def update(self, location_id, **kwargs):
        location = await self.get(location_id)
        if location:
            for key, value in kwargs.items():
                setattr(location, key, value)
            await self.objects.update(location)
            return location
        return None

    async def delete(self, location_id):
        location = await self.get(location_id)
        if location:
            await self.objects.delete(location)
            return location
        return None
