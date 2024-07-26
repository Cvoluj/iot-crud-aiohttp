from repositories.mixins import CreateRepositoryMixin, ReadRepositoryMixin, UpdateRepositoryMixin, DeleteRepositoryMixin
from repositories.base_repository import BaseRepository

class CRUDRepository(
    BaseRepository,
    CreateRepositoryMixin,
    ReadRepositoryMixin,
    UpdateRepositoryMixin,
    DeleteRepositoryMixin,
):
    pass