from database import get_async_database

class BaseRepository:
    def __init__(self, model):
        self.model = model
        self.objects = get_async_database()


    