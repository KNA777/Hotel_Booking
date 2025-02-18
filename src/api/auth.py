from os import access

from fastapi import HTTPException, Response
from fastapi import APIRouter, Body
from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectAlreadyExistsException, MailAlreadyExistHTTPException, UserMailAlreadyExist, \
    UserRegistrationPswException, UserRegistrationPswHTTPException, ObjectNotFoundException, \
    UserMailNotExistHTTPException, UserMailNotExistException, UserWrongEnterPswException, UserWrongEnterPswHTTPException
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
    except UserRegistrationPswException:
        raise UserRegistrationPswHTTPException

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
    try:
        access_token = await AuthService(db).login(response=response, data=data)
    except UserMailNotExistException:
        raise UserMailNotExistHTTPException
    except UserWrongEnterPswException:
        raise UserWrongEnterPswHTTPException
    return {"access_token": access_token}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
