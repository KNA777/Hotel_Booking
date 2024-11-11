from fastapi import APIRouter, Query, Path, Body
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.shemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение всех отелей")
async def get_all_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Идентификационный ключ отеля"),
        title: str | None = Query(None, description="Название отеля"),

):
    async with async_session_maker() as session:
        query_get_hotel = select(HotelsOrm).filter_by(id=id, title=title)
        res = await session.execute(query_get_hotel)
    return res.scalars().all()


@router.post("", summary="Добавление Отеля")
async def create_hotel(
        hotel_data: Hotel = Body(openapi_examples={
            "1": {"summary": "Москва", "value": {
                "title": "Redisson",
                "location": "Проспект Победы 77"

            }},
            "2": {"summary": "Тверь", "value": {
                "title": "Zvezda",
                "location": "Симеоновская 60"

            }},
            "3": {"summary": "Санкт-Петербург", "value": {
                "title": "Kovalevskaya",
                "location": "Невский проспект 100"

            }}})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(bind=engine, compile_kwargs={"literal_binds": True})) # Точный сырой запрос в БД
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Полное изменение отеля")
def full_change_hotel(
        hotel_data: Hotel,
        hotel_id: int = Path(description="Идентификационный ключ отеля"),

):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["address"] = hotel_data.address
        else:
            continue
    return {
        "status": "OK",
        "data": hotels
    }


@router.patch("/{hotel_id}", summary="Частичное изменение отеля")
def partial_change_hotel(
        hotel_data: HotelPatch,
        hotel_id: int = Path(description="Идентификационный ключ отеля"),

):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.address is not None:
                hotel["address"] = hotel_data.address
    return {
        "status": "OK",
        "data": hotels
    }


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(
        hotel_id: int = Path(description="Идентификационный ключ отеля")
):
    global hotels
    # hotels_ = []
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {
        "status": "OK",
        "all_hotels": hotels
    }
