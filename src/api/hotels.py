from datetime import date

from fastapi import APIRouter, Query, Path, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.shemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение всех отелей")
# @cache(expire=10)
async def get_all_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес отеля"),
        date_from: date = Query(example="2024-12-15"),
        date_to: date = Query(example="2024-12-19")

):
    return await db.hotels.get_filtered_by_time(
        location=location,
        title=title,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1),
        date_from=date_from,
        date_to=date_to
    )
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=pagination.per_page or 5,
    #     offset=pagination.per_page * (pagination.page - 1)
    # )
    #


@router.get("/{hotel_id}", summary="Получение одного отеля")
async def get_one_hotel(hotel_id: int, db: DBDep):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    return {
        "data": hotel
    }


@router.post("", summary="Добавление Отеля")
async def create_hotel(
        db: DBDep,
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "hotel": hotel}


@router.put("/{hotel_id}", summary="Полное изменение отеля")
async def full_change_hotel(
        db: DBDep,
        hotel_data: HotelAdd,
        hotel_id: int = Path(description="Идентификационный ключ отеля"),
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {
        "status": "OK"
    }


@router.patch("/{hotel_id}", summary="Частичное изменение отеля")
async def partial_change_hotel(
        db: DBDep,
        hotel_data: HotelPatch,
        hotel_id: int = Path(description="Идентификационный ключ отеля"),

):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(
        db: DBDep,
        hotel_id: int = Path(description="Идентификационный ключ отеля")
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {
        "status": "OK"
    }
