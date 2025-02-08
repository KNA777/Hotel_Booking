from fastapi import APIRouter
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException
from src.services.bookings import BookingService
from src.shemas.bookings import BookingsRequest, BookingsAdd


router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.get("", summary="Получение всех бронирований")
async def not_auth_all_bookings(db: DBDep):
    return await BookingService(db).all_bookings()


@router.get(
    "/me", summary="Получение всех бронирований для аутентифицированного пользователя"
)
async def auth_user_get_all_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).auth_user_all_bookings(user_id)


@router.post("", summary="Добавление бронирования")
async def add_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingsRequest):
    try:
        return await BookingService(db).create_bookings(user_id=user_id, booking_data=booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
