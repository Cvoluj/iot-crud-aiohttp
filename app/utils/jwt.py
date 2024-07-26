import jwt
from aiohttp import web
from config import server_setting



def get_user_id_from_jwt(request, algorithms=['HS256']):
    user_id = jwt.decode(
        get_token(get_auth_header(request)), 
        server_setting.SECRET_KEY, algorithms=['HS256']
    ).get('user_id')
    if not user_id:
        raise ValueError('Invalid token')
    return user_id

def get_auth_header(request):
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise web.HTTPUnauthorized
    return auth_header

def get_token(auth_header):
    scheme, token = auth_header.split(' ')
    if scheme.lower() != 'bearer':
        raise ValueError('Invalid authorization scheme')
    return token
