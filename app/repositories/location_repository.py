from repositories.crud_repository import CRUDRepository
from database.models import ApiUser, Location

class LocationRepository(CRUDRepository):
    async def get_join(self, *args, **kwargs):
        query = Location.select(Location, ApiUser).join(ApiUser).switch(Location)
        obj = await self.objects.get_or_none(query, *args, **kwargs)
        return obj if obj else 'None'