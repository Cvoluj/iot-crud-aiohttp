import logging
from aiohttp import web
from aiohttp.web import HTTPUnauthorized
from peewee import DoesNotExist

from database.models import ApiUser
from database import get_async_database
from utils.jwt import get_user_id_from_jwt

async def auth_middleware(app, handler):
    async def middleware_handler(request):
        objects = get_async_database()
        
        if not getattr(handler, 'require_login', False):
            return await handler(request)
        
        try:
            request.user = await objects.get(ApiUser, id=get_user_id_from_jwt(request))
        except HTTPUnauthorized:
            return web.Response(status=401, text='Missing authorization header')
        except DoesNotExist:
            return web.Response(status=401, text='Invalid Token')
        except Exception as e:
            logging.error('Error attempting to login user:', e)
            return web.Response(status=500, text='Internal server error')
        
        return await handler(request)
    
    return middleware_handler

def require_login(function):
    async def wrapper(*args, **kwargs):
        return await function(*args, **kwargs)
    wrapper.require_login = True
    return wrapper