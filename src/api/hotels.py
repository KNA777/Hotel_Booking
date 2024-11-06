from fastapi import APIRouter, Query, Path, Body
from src.api.dependencies import PaginationDep
from src.shemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [

    {"id": 1, "title": "Plaza", "address": "Sochi, Prospect Bobbed 137"},
    {"id": 2, "title": "Zvezda", "address": "Sochi, Kovalevskaya street 35"},
    {"id": 3, "title": "Abeda", "address": "Piter, Nevsky 100"},
    {"id": 4, "title": "Hostel", "address": "Piter, Svobody 44"},
    {"id": 5, "title": "Жемчужина", "address": "Казань, Остоженка 33"},
    {"id": 6, "title": "Piece", "address": "Voroneg, volodarskogo 64"},
    {"id": 7, "title": "gopa", "address": "Dubna, kujmisheva 234"},

]


@router.get("", summary="Получение всех отелей")
def get_all_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Идентификационный ключ отеля"),
        title: str | None = Query(None, description="Название отеля"),

):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]


@router.post("", summary="Добавление Отеля")
def add_hotel(
        hotel_data: Hotel = Body(openapi_examples={
            "1": {"summary": "Москва", "value": {
                "title": "Redisson",
                "address": "Проспект Победы 77"

            }},
            "2": {"summary": "Тверь", "value": {
                "title": "Zvezda",
                "address": "Симеоновская 60"

            }},
            "3": {"summary": "Санкт-Петербург", "value": {
                "title": "Kovalevskaya",
                "address": "Невский проспект 100"

            }}})
):
    global hotels
    new_hotel = {
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "address": hotel_data.address
    }
    hotels.append(new_hotel)
    return {
        "data": new_hotel
    }


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
