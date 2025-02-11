from datetime import date

from src.exceptions import check_date_from_to_date_to, HotelNotFoundHTTPException, ObjectNotFoundException, \
    HotelNotFoundException, RoomNotFoundException
from src.services.base import BaseService
from src.services.hotels import HotelService
from src.shemas.facilities import RoomFacilityAdd
from src.shemas.rooms import RoomsRequest, RoomAdd, RoomsRequestPatch, RoomPatch


class RoomService(BaseService):

    async def get_rooms_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        check_date_from_to_date_to(date_from, date_to)
        return await self.db.rooms.get_rooms_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, room_id: int, hotel_id: int):
        room =  await self.db.rooms.get_onewith_rels(id=room_id, hotel_id=hotel_id)
        return room

    async def crete_room(
            self,
            hotel_id: int,
            data_room: RoomsRequest):

        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
        new_data_room = RoomAdd(hotel_id=hotel_id, **data_room.model_dump())
        result = await self.db.rooms.add(new_data_room)
        rooms_facility_data = [
            RoomFacilityAdd(room_id=result.id, facility_id=f_id)
            for f_id in data_room.facilities_ids
        ]
        if rooms_facility_data:
            await self.db.facilities_rooms.add_bulk(rooms_facility_data)
        await self.db.commit()
        return result

    async def full_change_room(self, hotel_id: int, room_id: int, room_data: RoomsRequest):
        await HotelService(self.db).check_hotel_exist(hotel_id)
        await self.check_room_exist(hotel_id)
        room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(room_data, id=room_id)
        await self.db.facilities_rooms.set_new_facilities_rooms(
            room_id, facility_ids=room_data.facilities_ids
        )
        await self.db.commit()

    async def partial_change_room(self, hotel_id: int, room_id: int, data: RoomsRequestPatch
    ):
        await HotelService(self.db).check_hotel_exist(hotel_id)
        await self.check_room_exist(hotel_id)
        _room_data_dict = data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id)
        if "facilities_ids" in _room_data_dict:
            await self.db.facilities_rooms.set_new_facilities_rooms(
                room_id, facility_ids=_room_data_dict["facilities_ids"]
            )
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelService(self.db).check_hotel_exist(hotel_id)
        await self.check_room_exist(hotel_id)
        await self.db.rooms.delete(hotel_id=hotel_id, id=room_id)
        await self.db.commit()

    async def check_room_exist(self, room_id):
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
