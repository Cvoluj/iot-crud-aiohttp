import asyncio
import peewee_async
from aiohttp import web

from routes import setup_routes
from database.models import database
from utils.initialize_database import initialize_database

initialize_database()

objects = peewee_async.Manager(database)
database.set_allow_sync(False)

app = web.Application()
setup_routes(app)
web.run_app(app)