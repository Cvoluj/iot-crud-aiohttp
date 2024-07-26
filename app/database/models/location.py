from peewee import CharField, ForeignKeyField

from database.models import BaseModel, ApiUser
from database.mixins import PrimaryKeyMixin, TimestampMixin

class Location(PrimaryKeyMixin, TimestampMixin, BaseModel):
    name = CharField()
    api_user = ForeignKeyField(ApiUser, backref='location')
    
    class Meta:
        tablename = 'location'