from src.api.dependencies import UserIdDep
from src.exceptions import HotelNotFoundException, ObjectNotFoundException, AllRoomsAreBookedException
from src.services.base import BaseService
from src.shemas.bookings import BookingsRequest, BookingsAdd


class BookingService(BaseService):

    async def all_bookings(self):
        return await self.db.bookings.get_all()

    async def auth_user_all_bookings(self, user_id: UserIdDep):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def create_bookings(self, user_id: UserIdDep, booking_data: BookingsRequest):
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        hotel_id = room.hotel_id
        room_price: int = room.price
        add_bookings = BookingsAdd(
            **booking_data.model_dump(),
            user_id=user_id,
            price=room_price,
        )
        try:
            result = await self.db.bookings.add_bookings(add_bookings, hotel_id=hotel_id)
        except ObjectNotFoundException:
            raise AllRoomsAreBookedException
        await self.db.commit()
        return result
