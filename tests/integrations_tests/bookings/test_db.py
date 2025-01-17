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
    res = await db.bookings.add(bookings_data)
    read_res = await db.bookings.get_one_or_none()
    assert read_res
    id_bookings = (await db.bookings.get_filtered())[0].id
    put_bookings_data = BookingsAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(2024, 9, 10),
        date_to=date(2024, 9, 20),
        price=1000
    )
    await db.bookings.edit(put_bookings_data, id=id_bookings)
    result = await db.bookings.get_one_or_none(id=res.id)
    assert result
    await db.bookings.delete(id=res.id)
    res_delete = await db.bookings.get_one_or_none(id=res.id)
    assert not res_delete














    await db.commit()
