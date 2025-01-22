from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select, insert

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.shemas.bookings import BookingsRequest, BookingsAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_today_checkin(self):
        query = (
            select(self.model)
            .filter(self.model.date_from == datetime.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]


    async def add_bookings(self, data: BookingsAdd, hotel_id):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id)
        res = await self.session.execute(rooms_ids_to_get)
        result = res.scalars().all()

        if data.room_id not in result:
            raise HTTPException(status_code=400, detail="Нельзя забронировать этот номер")

        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)












        # rooms_to_get = (
        #     select(RoomsOrm)
        #     .select_from(RoomsOrm)
        #     .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        # )
        #
        #
        # # res = await self.session.execute(rooms_to_get)
        # # return [Rooms.model_validate(model, from_attributes=True) for model in res.scalars().all()]


