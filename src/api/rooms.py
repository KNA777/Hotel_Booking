from datetime import date
from fastapi import APIRouter, Query, HTTPException, Body
from pydantic import Field

from src.api.dependencies import DBDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException, \
    RoomNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException
from src.services.rooms import RoomService
from src.shemas.facilities import RoomFacilityAdd
from src.shemas.rooms import RoomsRequest, RoomAdd, RoomsRequestPatch, RoomPatch, Rooms

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров")
async def get_all_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2024-12-15"),
        date_to: date = Query(example="2024-12-19"),
):
    return await RoomService(db).get_rooms_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение одного номера")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms", summary="Добавление номера")
async def add_room(db: DBDep, hotel_id: int, data_room: RoomsRequest):
    try:
        room = await RoomService(db).crete_room(hotel_id, data_room)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"data": room}


@router.put("/{hotel_id}/rooms/{room_id}/{pok}", summary="Полное изменение атрибутов номера")
async def full_change_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomsRequest):
    await RoomService(db).full_change_room(hotel_id, room_id, room_data)
    return {"status": True}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное изменение атрибутов номера")
async def partial_change_room(
        db: DBDep, hotel_id: int, room_id: int, data: RoomsRequestPatch
):
    await RoomService(db).partial_change_room(hotel_id, room_id, data)
    return {"status": True}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": True}
