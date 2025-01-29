from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select, insert

from src.exceptions import AllRoomsAreBookedException
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.shemas.bookings import BookingsAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_today_checkin(self):
        query = select(self.model).filter(self.model.date_from == datetime.today())
        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]

    async def add_bookings(self, data: BookingsAdd, hotel_id):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id
        )
        res = await self.session.execute(rooms_ids_to_get)
        result = res.scalars().all()

        if data.room_id in result:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise AllRoomsAreBookedException

