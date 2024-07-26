import logging
from aiohttp import web

from utils import model_to_dict
from middlewares import require_login
from utils.jwt import get_user_id_from_jwt
from services import LocationService
from database.models import Location, ApiUser


class LocationHandler:
    def __init__(self, location_service: LocationService):
        self.location_service = location_service
        self.logger = logging.getLogger(__name__)

    @require_login
    async def create_location(self, request):
        try:
            data = await request.json()
            data['api_user_id'] =  get_user_id_from_jwt(request)
            location: Location = await self.location_service.get_location(**data)
            if location != 'None':
                return web.Response(status=409, text='You already have that location')
            
            location: Location = await self.location_service.create_location(**data)
            return web.json_response({
                    "id": location.id,
                    "name": location.name,
                    "api_user_id": data['api_user_id'],
            })
            
        except Exception as e:
            self.logger.error(f"Error creating location: {e}")
            return web.Response(status=500, text='Internal Server Error')

    @require_login
    async def get_location(self, request):
        try:
            data = await request.json()
            data['api_user_id'] =  get_user_id_from_jwt(request)
            location: Location = await self.location_service.get_join(name=data.get('name'), api_user_id=data['api_user_id'])
            user: ApiUser = location.api_user
            
            if user.id != data['api_user_id']:
                return web.Response(status=401, text="It's not your location")
                        
            if location == 'None':
                return web.Response(status=404, text='Location not found')
            
            return web.json_response({
                    "id": location.id,
                    "name": location.name,
                    "api_user_id": user.id,
            })
        except Exception as e:
            self.logger.error(f"Error getting location: {e}")
            return web.Response(status=500, text='Internal Server Error')

    @require_login
    async def update_location(self, request):
        try:
            data = await request.json()
            id = request.match_info.get('id')
            api_user_id =  get_user_id_from_jwt(request)
            location: Location = await self.location_service.get_join(id)
            user: ApiUser = location.api_user
            
            if user.id != api_user_id:
                return web.Response(status=401, text="It's not your location")
                        
            if location == 'None':
                return web.Response(status=404, text='Location not found')
            
            await self.location_service.update_location(location.id, **data)
            location: Location = await self.location_service.get_join(id)
            
            return web.json_response({
                    "id": location.id,
                    "name": location.name,
                    "api_user_id": user.id,
            })
        except Exception as e:
            self.logger.error(f"Error getting location: {e}")
            return web.Response(status=500, text='Internal Server Error')

    @require_login
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
