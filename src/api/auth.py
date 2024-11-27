from fastapi import HTTPException, Response, Request
from fastapi import APIRouter, Body
from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.services.auth import AuthService
from src.shemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(data: UserRequestAdd = Body(openapi_examples={
    "1": {"summary": "user1", "value": {
        "email": "yandex@yandex.ru",
        "password": "12345678"
    }}
})):
    hashed_password = AuthService.hashed_password(data.password)
    user_add_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(user_add_data)
        await session.commit()
        return {"status": "OK"}


@router.post("/login")
async def login_user(
        response: Response,
        data: UserRequestAdd = Body(openapi_examples={
            "1": {"summary": "user1", "value": {
                "email": "yandex@yandex.ru",
                "password": "12345678"
            }}
        })):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_psw(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден с данной почтой")
        if not AuthService.verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Введен неверный пароль")
        access_token = AuthService.create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/me")
async def get_me(
        user_id: UserIdDep
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {
        "status": "OK"
    }

