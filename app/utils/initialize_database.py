from database.models import ApiUser, Location, Device

def initialize_database(database):
    with database.connection_context():
        database.create_tables([ApiUser, Location, Device])
