from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.shemas.rooms import RoomsRequest, RoomAdd, RoomsRequestPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров")
async def get_all_rooms(db: DBDep, hotel_id: int):
    result = await db.rooms.get_filtered(hotel_id=hotel_id)
    if result:
        return result
    return "Мы не нашли ни одного номера в данном отеле"


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
        await db.rooms.edit(data, hotel_id=hotel_id, id=room_id)
        await db.commit()
        return {"status": True}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение атрибутов номера")
async def partial_change_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        data: RoomsRequestPatch):
    await db.rooms.edit(data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": True}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": True}
