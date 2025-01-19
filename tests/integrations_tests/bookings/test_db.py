from datetime import date

from src.shemas.bookings import BookingsAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    bookings_data = BookingsAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(2024, 8, 10),
        date_to=date(2024, 8, 20),
        price=100
    )
    new_booking = await db.bookings.add(bookings_data)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    # Обновление брони
    updated_date = date(2024, 9, 20)
    update_bookings_data = BookingsAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(2024, 9, 10),
        date_to=updated_date,
        price=1000
    )
    await db.bookings.edit(update_bookings_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == updated_date

    # Удаление брони

    await db.bookings.delete(id=new_booking.id)
    booking_delete = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking_delete
