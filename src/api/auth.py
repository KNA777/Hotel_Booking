from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.repositories.users import UsersRepository
from src.shemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(data: UserRequestAdd = Body(openapi_examples={
        "1": {"summary": "user1", "value": {
            "email": "yandex@yandex.ru",
            "password": "12345678"
        }}
})):
    hashed_password = None
    user_add_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        hotel = await UsersRepository(session).add_hotel(data)
        await session.commit()
        return {"status": "OK"}

