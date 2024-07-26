import peewee_async
from database.database import database

def get_async_database() -> peewee_async.Manager: 
    objects = peewee_async.Manager(database)
    database.set_allow_sync(False)
    return objects