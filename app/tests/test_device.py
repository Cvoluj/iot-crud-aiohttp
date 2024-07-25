# tests/test_device.py
import pytest
import asyncio
from aiohttp import web
from utils.initialize_database import initialize_database
from repositories.device_repository import DeviceRepository
from services.device_service import DeviceService
from handlers.device_handler import DeviceHandler
from config import server_setting
import peewee_async

@pytest.fixture
def database():
    test_db = peewee_async.PooledPostgresqlDatabase(
        server_setting.TEST_POSTGRES_DATABASE,
        max_connections=20,
        user=server_setting.TEST_POSTGRES_USER,
        password=server_setting.TEST_POSTGRES_PASSWORD,
        host=server_setting.DB_HOST,
        port=server_setting.DB_PORT,
    )
    return test_db


@pytest.fixture
def cli(event_loop, aiohttp_client, database):

    initialize_database(database)

    device_repository = DeviceRepository(database)
    device_service = DeviceService(device_repository)
    device_handler = DeviceHandler(device_service)

    app = web.Application()
    app.router.add_post('/devices', device_handler.create_device)
    app.router.add_get('/devices/{id}', device_handler.get_device)
    app.router.add_put('/devices/{id}', device_handler.update_device)
    app.router.add_delete('/devices/{id}', device_handler.delete_device)
    
    return event_loop.run_until_complete(aiohttp_client(app))

@pytest.fixture
def create_device_payload():
    return {
        'name': 'Test Device',
        'device_type': 'Sensor',
        'login': 'test_login',
        'password': 'test_password',
        'location_id': 1,
        'api_user_id': 1
    }

@pytest.mark.asyncio
async def test_create_device(cli, create_device_payload):
    resp = await cli.post('/devices', json=create_device_payload)
    assert resp.status == 200
    data = await resp.json()
    assert 'id' in data

@pytest.mark.asyncio
async def test_get_device(cli, create_device_payload):
    create_resp = await cli.post('/devices', json=create_device_payload)
    device_id = (await create_resp.json())['id']

    get_resp = await cli.get(f'/devices/{device_id}')
    assert get_resp.status == 200
    device_data = await get_resp.json()
    assert device_data['name'] == create_device_payload['name']

@pytest.mark.asyncio
async def test_update_device(cli, create_device_payload):
    create_resp = await cli.post('/devices', json=create_device_payload)
    device_id = (await create_resp.json())['id']

    update_payload = {'name': 'Updated Device'}
    update_resp = await cli.put(f'/devices/{device_id}', json=update_payload)
    assert update_resp.status == 200

    get_resp = await cli.get(f'/devices/{device_id}')
    device_data = await get_resp.json()
    assert device_data['name'] == 'Updated Device'

@pytest.mark.asyncio
async def test_delete_device(cli, create_device_payload):
    create_resp = await cli.post('/devices', json=create_device_payload)
    device_id = (await create_resp.json())['id']

    delete_resp = await cli.delete(f'/devices/{device_id}')
    assert delete_resp.status == 200

    get_resp = await cli.get(f'/devices/{device_id}')
    assert get_resp.status == 404
