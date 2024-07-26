import logging
from aiohttp import web
from services import DeviceService


class DeviceHandler:
    def __init__(self, device_service: DeviceService):
        self.device_service = device_service
        self.logger = logging.getLogger(__name__)

    async def create_device(self, request):
        try:
            user = request.user
            data = await request.json()
            data['api_user_id'] = user.id
            device = await self.device_service.create_device(**data)
            return web.json_response({'id': device.id})
        except Exception as e:
            self.logger.error(f"Error creating device: {e}")
            return web.Response(status=500, text=str(e))

    async def get_device(self, request):
        try:
            user = request.user
            device_id = int(request.match_info['id'])
            device = await self.device_service.get_device(device_id)
            if device and device.api_user.id == user.id:
                return web.json_response(device)
            return web.Response(status=404, text="Device not found or not owned by user")
        except Exception as e:
            self.logger.error(f"Error getting device: {e}")
            return web.Response(status=500, text=str(e))

    async def update_device(self, request):
        try:
            user = request.user
            device_id = int(request.match_info['id'])
            device = await self.device_service.get_device(device_id)
            if not device or device.api_user.id != user.id:
                return web.Response(status=404, text="Device not found or not owned by user")
            
            data = await request.json()
            await self.device_service.update_device(device_id, data)
            return web.Response(status=200)
        except Exception as e:
            self.logger.error(f"Error updating device: {e}")
            return web.Response(status=500, text=str(e))

    async def delete_device(self, request):
        try:
            user = request.user
            device_id = int(request.match_info['id'])
            device = await self.device_service.get_device(device_id)
            if not device or device.api_user.id != user.id:
                return web.Response(status=404, text="Device not found or not owned by user")
            
            await self.device_service.delete_device(device_id)
            return web.Response(status=200)
        except Exception as e:
            self.logger.error(f"Error deleting device: {e}")
            return web.Response(status=500, text=str(e))
