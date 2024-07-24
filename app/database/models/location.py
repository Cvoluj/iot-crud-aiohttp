from peewee import CharField

from database.models import BaseModel
from database.mixins import PrimaryKeyMixin, TimestampMixin

class Location(PrimaryKeyMixin, TimestampMixin, BaseModel):
    name = CharField()
    
    class Meta:
        tablename = 'location'