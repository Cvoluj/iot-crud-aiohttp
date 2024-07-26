from repositories import LocationRepository

class LocationService:
    def __init__(self, location_repository: LocationRepository):
        self.location_repository = location_repository

    async def create_location(self, **kwargs):
        return await self.location_repository.create(**kwargs)

    async def get_location(self, location_id):
        return await self.location_repository.get(location_id)

    async def update_location(self, location_id, **kwargs):
        return await self.location_repository.update(location_id, **kwargs)

    async def delete_location(self, location_id):
        return await self.location_repository.delete(location_id)