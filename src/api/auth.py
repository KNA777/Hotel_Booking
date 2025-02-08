from fastapi import HTTPException, Response
from fastapi import APIRouter, Body
from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectAlreadyExistsException, MailAlreadyExistHTTPException, UserMailAlreadyExist
from src.services.auth import AuthService
from src.shemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "user1",
                "value": {"email": "yandex@yandex.ru", "password": "12345678"},
            }
        }
    ),
):
    try:
        await AuthService(db).register(data)
    except UserMailAlreadyExist:
        raise MailAlreadyExistHTTPException

    return {"status": "OK"}


@router.post("/login")
async def login_user(
    db: DBDep,
    response: Response,
    data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "user1",
                "value": {"email": "yandex@yandex.ru", "password": "12345678"},
            }
        }
    ),
):
    user = await db.users.get_user_with_hashed_psw(email=data.email)
    if not user:
        raise HTTPException(
            status_code=401, detail="Пользователь не найден с данной почтой"
        )
    if not AuthService.verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Введен неверный пароль")
    access_token = AuthService.create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
