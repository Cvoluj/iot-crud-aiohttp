from database.database import database
from database.models import ApiUser, Location, Device

def initialize_database():
    with database.connection_context():
        database.create_tables([ApiUser, Location, Device])
