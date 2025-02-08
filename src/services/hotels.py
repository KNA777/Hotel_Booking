from datetime import date

from fastapi import HTTPException

from src.exceptions import HotelNotFoundException, ObjectNotFoundException
from src.services.base import BaseService
from src.shemas.hotels import HotelAdd, HotelPatch


class HotelService(BaseService):

    async def get_hotels(self,
                         pagination,
                         title: str | None,
                         location: str | None,
                         date_from: date,
                         date_to: date):
        if date_from >= date_to:
            raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")
        return await self.db.hotels.get_filtered_by_time(
            location=location,
            title=title,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
            date_from=date_from,
            date_to=date_to,
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel


    async def full_change_hotel(self, data: HotelAdd, hotel_id: int):
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()


    async def partial_change_hotel(self, data: HotelPatch, hotel_id: int):
        await self.db.hotels.edit(data, exclude_unset=True, id=hotel_id)
        await self.db.commit()


    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()


    async def check_hotel_exist(self, hotel_id):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException

