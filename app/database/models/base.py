from peewee import Model
from database.database import database

class BaseModel(Model):
    
    class Meta:
        database = database