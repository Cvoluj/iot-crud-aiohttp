# handlers/device_handler.py
import logging
from aiohttp import web
from services import DeviceService


class DeviceHandler:
    def __init__(self, device_service: DeviceService):
        self.device_service = device_service
        self.logger = logging.getLogger(__name__)

    async def create_device(self, request):
        try:
            data = await request.json()
            print(data)
            device = await self.device_service.create_device(**data)
            return web.json_response({'id': device.id})
        except Exception as e:
            self.logger.error(f"Error creating device: {e}")
            return web.Response(status=500, text=str(e))

    async def get_device(self, request):
        try:
            device_id = int(request.match_info['id'])
            device = self.device_service.get_device(device_id)
            if device:
                return web.json_response(device)
            return web.Response(status=404, text="Device not found")
        except Exception as e:
            self.logger.error(f"Error getting device: {e}")
            return web.Response(status=500, text=str(e))

    async def update_device(self, request):
        try:
            device_id = int(request.match_info['id'])
            data = await request.json()
            self.device_service.update_device(device_id, data)
            return web.Response(status=200)
        except Exception as e:
            self.logger.error(f"Error updating device: {e}")
            return web.Response(status=500, text=str(e))

    async def delete_device(self, request):
        try:
            device_id = int(request.match_info['id'])
            self.device_service.delete_device(device_id)
            return web.Response(status=200)
        except Exception as e:
            self.logger.error(f"Error deleting device: {e}")
            return web.Response(status=500, text=str(e))
