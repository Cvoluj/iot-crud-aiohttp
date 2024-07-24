from peewee import CharField

from database.models import BaseModel
from database.mixins import TimestampMixin, PrimaryKeyMixin

class ApiUser(BaseModel, PrimaryKeyMixin, TimestampMixin):
    
    name = CharField()
    email = CharField(unique=True)
    password = CharField()
    
    class Meta:
        tablename = 'api_user'