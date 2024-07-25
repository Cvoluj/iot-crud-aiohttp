import asyncio
from aiohttp import web
import aiohttp

from database.database import database
from utils.initialize_database import initialize_database
from repositories.device_repository import DeviceRepository
from services import DeviceService
from handlers import DeviceHandler

initialize_database(database)

device_repository = DeviceRepository(database)
device_service = DeviceService(device_repository)
device_handler = DeviceHandler(device_service)

app = web.Application()
app.router.add_post('/devices', device_handler.create_device)
app.router.add_get('/devices/{id}', device_handler.get_device)
app.router.add_put('/devices/{id}', device_handler.update_device)
app.router.add_delete('/devices/{id}', device_handler.delete_device)


async def main():
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner)    
    await site.start()
    await asyncio.Event().wait()    

if __name__ == '__main__':
    asyncio.run(main())