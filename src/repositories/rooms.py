from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.shemas.rooms import Rooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms
