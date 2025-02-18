from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, Response

from src.config import settings
from passlib.context import CryptContext
import jwt

from src.exceptions import ObjectAlreadyExistsException, UserMailAlreadyExist, ObjectNotFoundException, \
    UserMailNotExistException, UserWrongEnterPswException, UserRegistrationPswException
from src.services.base import BaseService
from src.shemas.users import UserRequestAdd, UserAdd


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str):
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")

    @classmethod
    def hashed_password(cls, password):
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    async def register(self, data: UserRequestAdd):
        if len(data.password) < 6:
            raise UserRegistrationPswException
        hashed_password = self.hashed_password(data.password)
        user_add_data = UserAdd(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(user_add_data)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise UserMailAlreadyExist

    async def login(self, response: Response, data: UserRequestAdd):
        try:
            user = await self.db.users.get_user_with_hashed_psw(email=data.email)
        except ObjectNotFoundException:
            raise UserMailNotExistException
        if not AuthService.verify_password(data.password, user.hashed_password):
            raise UserWrongEnterPswException
        access_token = AuthService.create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return access_token