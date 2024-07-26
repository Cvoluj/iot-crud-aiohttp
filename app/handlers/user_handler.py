import jwt
import bcrypt
import logging
from aiohttp import web
from peewee import DoesNotExist
from services import UserService
from database.models import ApiUser

from utils import model_to_dict
from config import server_setting
from middlewares import require_login
from utils import get_user_id_from_jwt

class UserHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.logger = logging.getLogger(__name__)

    async def create_user(self, request):
        try:
            data = await request.json()
            data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user_already_exists = await self.user_service.get_user(email=data.get('email'))
            if user_already_exists != 'None':
                return web.Response(status=409, text='User with this email already exists')
            user: ApiUser = await self.user_service.create_user(**data)
            return web.json_response({
                'id': user.id,
                'email': user.email,
                'name': user.name,
            })
            
        except Exception as e:
            self.logger.error(f"Error creating user: {e}")
            return web.Response(status=500, text='Internal Server Error')

    @require_login
    async def get_user(self, request):
        try:            
            id = request.match_info.get('id')
            user: ApiUser | 'None' = await self.user_service.get_user(id=id)
            if user != 'None':
                return web.json_response(model_to_dict(user, exclude=['password']))
            return web.Response(status=404, text="User not found")
        except Exception as e:
            self.logger.error(f"Error getting user: {e}")
            return web.Response(status=500, text='Internal Server Error')
    
    @require_login
    async def update_user(self, request):
        try:
            logged_user_id = get_user_id_from_jwt(request)
            id = request.match_info.get('id')
            
            if int(logged_user_id) != int(id):
                return web.Response(status=401, text='You have no permission to change other user info')
            
            data: dict = await request.json()
            if 'password' in data:
                data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            await self.user_service.update_user(id, **data)
            return web.json_response(model_to_dict(await self.user_service.get_user(id=id), exclude=['password']))
        except Exception as e:
            self.logger.error(f"Error updating user: {e}")
            return web.Response(status=500, text='Internal Server Error')

    @require_login
    async def delete_user(self, request):
        try:
            logged_user_id = get_user_id_from_jwt(request)
            id = request.match_info.get('id')
            
            if int(logged_user_id) != int(id):
                return web.Response(status=401, text='You have no permission to delete other user profile')
        
            await self.user_service.delete_user(id)
            return web.Response(status=200)
        except DoesNotExist:
            return web.Response(status=404, text='Not found') 
        except Exception as e:
            self.logger.error(f"Error deleting user: {e}")
            return web.Response(status=500, text='Internal Server Error')

    async def login(self, request):
        try:
            data = await request.json()
            user = await self.user_service.get_user(email=data['email'])
            if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'user_id': user.id}, server_setting.SECRET_KEY, algorithm='HS256')
                return web.json_response({'token': token})
            return web.Response(status=401, text="Invalid email or password")
        except Exception as e:
            self.logger.error(f"Error logging in: {e}")
            return web.Response(status=500, text='Internal Server Error')
