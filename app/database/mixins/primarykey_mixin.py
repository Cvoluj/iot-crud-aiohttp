from peewee import Model, AutoField

from database.database import database

class PrimaryKeyMixin(Model):
    id = AutoField()

    class Meta:
        database = database
        abstract = True