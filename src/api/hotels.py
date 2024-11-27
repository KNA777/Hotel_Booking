from fastapi import APIRouter, Query, Path, Body
from src.api.dependencies import PaginationDep
from src.config import settings
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.shemas.hotels import Hotel, HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение всех отелей")
async def get_all_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес отеля")

):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=pagination.per_page or 5,
            offset=pagination.per_page * (pagination.page - 1)
        )


@router.post("", summary="Добавление Отеля")
async def create_hotel(
        hotel_data: HotelAdd = Body(openapi_examples={
            "1": {"summary": "Москва", "value": {
                "title": "Redisson",
                "location": "Москва, Проспект Победы 77"

            }},
            "2": {"summary": "Тверь", "value": {
                "title": "Zvezda",
                "location": "Тверь, Симеоновская 60"

            }},
            "3": {"summary": "Санкт-Петербург", "value": {
                "title": "Kovalevskaya",
                "location": "Санкт-Петербург, Невский проспект 100"

            }}})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
        return {"status": "OK", "hotel": hotel}


@router.put("/{hotel_id}", summary="Полное изменение отеля")
async def full_change_hotel(
        hotel_data: HotelAdd,
        hotel_id: int = Path(description="Идентификационный ключ отеля"),

):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
        return {
            "status": "OK"
        }


@router.patch("/{hotel_id}", summary="Частичное изменение отеля")
async def partial_change_hotel(
        hotel_data: HotelPatch,
        hotel_id: int = Path(description="Идентификационный ключ отеля"),

):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(
        hotel_id: int = Path(description="Идентификационный ключ отеля")
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
        return {
            "status": "OK"
        }

@router.get("/{hotel_id}", summary="Получение одного отеля")
async def get_one_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        return {
            "data": hotel
        }
