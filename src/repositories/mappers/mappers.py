from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.shemas.bookings import Bookings
from src.shemas.facilities import Facility
from src.shemas.hotels import Hotel
from src.shemas.rooms import Rooms, RoomsWithRels
from src.shemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Rooms


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomsWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Bookings


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility
