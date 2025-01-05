from datetime import date
from fastapi import APIRouter, Query
from src.api.dependencies import DBDep
from src.shemas.facilities import RoomFacilityAdd
from src.shemas.rooms import RoomsRequest, RoomAdd, RoomsRequestPatch, RoomPatch, Rooms

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров")
async def get_all_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2024-12-15"),
        date_to: date = Query(example="2024-12-19")
):
    result = await db.rooms.get_rooms_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    if result:
        return result
    return {"data": "Мы не нашли ни одного номера в данном отеле"}


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение одного номера")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    res = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if not res:
        return f"Мы не нашли такой комнаты в данном отеле с {hotel_id} id"
    return res


@router.post("/{hotel_id}/rooms", summary="Добавление номера")
async def add_room(
        db: DBDep,
        hotel_id: int,
        data_room: RoomsRequest):
    new_data_room = RoomAdd(hotel_id=hotel_id, **data_room.model_dump())
    result = await db.rooms.add(new_data_room)
    rooms_facility_data = [RoomFacilityAdd(room_id=result.id, facility_id=f_id) for f_id in data_room.facilities_ids]
    await db.facilities_rooms.add_bulk(rooms_facility_data)
    await db.commit()
    return {
        "data": result
    }


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное изменение атрибутов номера")
async def full_change_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        data: RoomsRequest):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    await db.rooms.edit(room_data, id=room_id)
    await db.facilities_rooms.set_new_facilities_rooms(room_id, facility_ids=data.facilities_ids)
    await db.commit()
    return {"status": True}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение атрибутов номера")
async def partial_change_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        data: RoomsRequestPatch):
    _room_data_dict = data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id)
    if "facilities_ids" in _room_data_dict:
        await db.facilities_rooms.set_new_facilities_rooms(room_id, facility_ids=_room_data_dict["facilities_ids"])
    await db.commit()
    return {"status": True}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": True}
