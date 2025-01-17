import json
import pytest

from httpx import AsyncClient

from src.config import settings
from src.contex_manager.db_manager import DBManager
from src.database import BaseOrm, engine_null_pool, async_session_maker_null_poll, async_session_maker
from src.main import app
from src.shemas.hotels import HotelAdd
from src.shemas.rooms import RoomAdd
from src.models import *


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async with DBManager(async_session_maker_null_poll) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as connect:
        await connect.run_sync(BaseOrm.metadata.drop_all)
        await connect.run_sync(BaseOrm.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def add_data_hotel(register_user):
    with open(file="tests/mock_rooms.json", mode="r", encoding="utf-8") as file:
        data_rooms = json.load(file)
    data_r = [RoomAdd.model_validate(el) for el in data_rooms]
    with open(file="tests/mock_hotels.json", mode="r", encoding="utf-8") as file:
        data_hotels = json.load(file)
    data_h = [HotelAdd.model_validate(el) for el in data_hotels]

    async with DBManager(async_session_maker_null_poll) as db_:
        await db_.hotels.add_bulk(data_h)
        await db_.rooms.add_bulk(data_r)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac(setup_database) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "kot@pes.com",
            "password": "1234"
        })
