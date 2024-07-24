from peewee import DateTimeField, Model
from datetime import datetime

from database.database import database

class TimestampMixin(Model):
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now(datetime.UTC)
        return super().save(*args, **kwargs)

    class Meta:
        database = database
        abstract = True