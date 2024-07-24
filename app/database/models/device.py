from peewee import CharField, ForeignKeyField

from database.models import BaseModel, ApiUser, Location
from database.mixins import PrimaryKeyMixin, TimestampMixin

class Device(PrimaryKeyMixin, TimestampMixin, BaseModel):
    
    name = CharField()
    device_type = CharField()
    login = CharField()
    password = CharField()
    location = ForeignKeyField(Location, backref='device')
    api_user = ForeignKeyField(ApiUser, backref='device')
    
    class Meta:
        tablename = 'device'