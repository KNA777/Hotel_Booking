from datetime import date

from fastapi import HTTPException


class AuthUserExceptions(Exception):
    detail = "Ошибка аутентификации/авторизации пользователя"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, **kwargs)


class UserMailAlreadyExist(AuthUserExceptions):
    detail = "Ошибка регистрации пользователя почта уже существует"

class BookingsExceptions(Exception):
    detail = "ОШИБКА"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, **kwargs)


class ObjectNotFoundException(BookingsExceptions):
    detail = "Объект не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Комната не найдена"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class ObjectAlreadyExistsException(BookingsExceptions):
    detail = "Похожий объект уже существует"


class AllRoomsAreBookedException(BookingsExceptions):
    detail = "Не осталось свободных номеров"


class UserExistException(BookingsExceptions):
    detail = "Пользователь с такой почтой уже существует"


def check_date_from_to_date_to(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


class BookingsHTTPExceptions(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BookingsHTTPExceptions):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(BookingsHTTPExceptions):
    status_code = 404
    detail = "Номер не найден"

class MailAlreadyExistHTTPException(BookingsHTTPExceptions):
    status_code = 422
    detail = "Почта уже существует"


class AllRoomsAreBookedHTTPException(BookingsHTTPExceptions):
    status_code = 404
    detail = "Не осталось свободных номеров"