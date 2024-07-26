import asyncio
from aiohttp import web
import aiohttp

from database.database import database
from database.models import ApiUser, Location, Device
from utils.initialize_database import initialize_database
from repositories import DeviceRepository, LocationRepository, UserRepository
from services import DeviceService, LocationService, UserService
from handlers import DeviceHandler, LocationHandler, UserHandler

from middlewares import auth_middleware

initialize_database(database)

device_repository = DeviceRepository(Device)
device_service = DeviceService(device_repository)
device_handler = DeviceHandler(device_service)

location_repository = LocationRepository(Location)
location_service = LocationService(location_repository)
location_handler = LocationHandler(location_service)

user_repository = UserRepository(ApiUser)
user_service = UserService(user_repository)
user_handler = UserHandler(user_service)

midllewares = [
    auth_middleware,
]

app = web.Application(
    middlewares=midllewares
    )
app.router.add_post('/devices', device_handler.create_device)
app.router.add_get('/devices/{id}', device_handler.get_device)
app.router.add_put('/devices/{id}', device_handler.update_device)
app.router.add_delete('/devices/{id}', device_handler.delete_device)

app.router.add_post('/users', user_handler.create_user)
app.router.add_get('/users/{id}', user_handler.get_user)
app.router.add_put('/users/{id}', user_handler.update_user)
app.router.add_delete('/users/{id}', user_handler.delete_user)

app.router.add_post('/login', user_handler.login)

app.router.add_post('/location', location_handler.create_location)
app.router.add_get('/location/{id}', location_handler.get_location)
app.router.add_put('/location/{id}', location_handler.update_location)
app.router.add_delete('/location/{id}', location_handler.delete_location)


async def main():
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner)    
    await site.start()
    await asyncio.Event().wait()    

if __name__ == '__main__':
    loop = asyncio.SelectorEventLoop()
    asyncio.set_event_loop(loop)
    web.run_app(app=app, loop=loop)