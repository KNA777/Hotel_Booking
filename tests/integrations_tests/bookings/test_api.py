import pytest

from tests.conftest import db_null_pool


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-02", "2024-08-11", 200),
    (1, "2024-08-03", "2024-08-12", 200),
    (1, "2024-08-04", "2024-08-13", 200),
    (1, "2024-08-05", "2024-08-14", 200),
    (1, "2024-08-06", "2024-08-15", 404),

])
async def test_add_booking(
        db, auth_ac,
        room_id, date_from, date_to, status_code):
    # room_id = (await db.rooms.get_all())[0].id
    response = await auth_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        assert isinstance(response.json(), dict)


# ОЧИСТКА ТАБЛИЦЫ ОТ ДАННЫХ ПЕРЕД ТЕСТОМ (СЫРОЙ ЗАПРОС)
# from sqlalchemy import text

# @pytest.fixture(scope="session")
# async def del_data_bookings():
#     async with engine_null_pool.begin() as connect:
#         await connect.execute(text("DELETE FROM bookings"))
#     await engine_null_pool.dispose()


@pytest.fixture(scope="module")
async def del_data_bookings():
    async for db_ in db_null_pool():
        await db_.bookings.delete()
        await db_.commit()

@pytest.mark.parametrize("room_id, date_from, date_to, count_booking, status_code", [
    (1, "2024-08-01", "2024-08-10", 1, 200),
    (2, "2024-08-02", "2024-08-11", 2, 200),
    (3, "2024-08-03", "2024-08-12", 3, 200),
])
async def test_count_bookings(
        room_id, date_from, date_to, count_booking, status_code,
                                    del_data_bookings, auth_ac,):
    response = await auth_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    assert response.status_code == status_code
    res = await auth_ac.get("/bookings/me")
    print(res.json())
    assert len(res.json()) == count_booking
