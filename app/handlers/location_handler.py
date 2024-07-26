import logging
from aiohttp import web

from utils.jwt import get_user_id_from_jwt
from services import LocationService

class LocationHandler:
    def __init__(self, location_service: LocationService):
        self.location_service = location_service
        self.logger = logging.getLogger(__name__)

    async def create_location(self, request):
        logged_user_id = get_user_id_from_jwt(request)

        
        try:
            data = await request.json()
            location = await self.location_service.create_location(**data, **{'user'})
            return web.json_response({'id': location.id})
        except Exception as e:
            self.logger.error(f"Error creating location: {e}")
            return web.Response(status=500, text='Internal Server Error')

    async def get_location(self, request):
        if not getattr(request, 'user', None):
            return web.Response(status=401, text="Unauthorized")

        try:
            location_id = int(request.match_info['id'])
            location = await self.location_service.get_location(location_id)
            if location:
                return web.json_response(location)
            return web.Response(status=404, text="Location not found")
        except Exception as e:
            self.logger.error(f"Error getting location: {e}")
            return web.Response(status=500, text='Internal Server Error')

    async def update_location(self, request):
        if not getattr(request, 'user', None):
            return web.Response(status=401, text="Unauthorized")

        try:
            location_id = int(request.match_info['id'])
            data = await request.json()
            await self.location_service.update_location(location_id, **data)
            return web.Response(status=200)
        except Exception as e:
            self.logger.error(f"Error updating location: {e}")
            return web.Response(status=500, text='Internal Server Error')

    async def delete_location(self, request):
        if not getattr(request, 'user', None):
            return web.Response(status=401, text="Unauthorized")

        try:
            location_id = int(request.match_info['id'])
            await self.location_service.delete_location(location_id)
            return web.Response(status=200)
        except Exception as e:
            self.logger.error(f"Error deleting location: {e}")
            return web.Response(status=500, text='Internal Server Error')
