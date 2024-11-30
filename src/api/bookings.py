from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.shemas.bookings import BookingsRequest, BookingsAdd

router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.post("", summary="Добавление бронирования")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingsRequest
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    add_bookings = BookingsAdd(**booking_data.model_dump(), user_id=user_id, price=room.price)
    result = await db.bookings.add(add_bookings)
    await db.commit()
    return result
