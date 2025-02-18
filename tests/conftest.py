# ruff: noqa: E402
import json
import pytest

from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from httpx import AsyncClient

from src.api.dependencies import get_db
from src.config import settings
from src.contex_manager.db_manager import DBManager
from src.database import BaseOrm, engine_null_pool, async_session_maker_null_poll
from src.main import app
from src.shemas.hotels import HotelAdd
from src.shemas.rooms import RoomAdd
from src.models import *    # noqa: F403


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"

async def db_null_pool():      # -> DBManager
    async with DBManager(async_session_maker_null_poll) as db:
        yield db

@pytest.fixture(scope="function")  # -> DBManager
async def db() -> DBManager:
    async for db in db_null_pool():
        yield db


# Перезписывание зависимости DBManager для тестов api
app.dependency_overrides[get_db] = db_null_pool


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
            "password": "12345678"
        })

@pytest.fixture(scope="session")
async def auth_ac(ac, register_user):
    await ac.post(
        "/auth/login",
        json={
            "email": "kot@pes.com",
            "password": "12345678",
        }
    )
    assert ac.cookies["access_token"]
    yield ac























