import peewee_async
from settings import server_setting

database = peewee_async.PooledPostgresqlDatabase(
    server_setting.POSTGRES_DATABASE,
    max_connections=20,
    user=server_setting.POSTGRES_USER,
    password=server_setting.POSTGRES_PASSWORD,
    host=server_setting.DB_HOST,
    port=server_setting.DB_PORT,
    )