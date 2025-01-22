from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.shemas.bookings import BookingsRequest, BookingsAdd

router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.get("", summary="Получение всех бронирований")
async def not_auth_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получение всех бронирований для аутентифицированного пользователя")
async def auth_user_get_all_bookings(
        db: DBDep,
        user_id: UserIdDep
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Добавление бронирования")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingsRequest
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    hotel_id = room.hotel_id
    room_price: int = room.price
    add_bookings = BookingsAdd(
        **booking_data.model_dump(),
        user_id=user_id,
        price=room_price,
        )
    result = await db.bookings.add_bookings(add_bookings, hotel_id=hotel_id)
    await db.commit()
    return result
