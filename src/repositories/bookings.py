from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.shemas.bookings import Bookings


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Bookings
