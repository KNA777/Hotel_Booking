from pydantic import EmailStr, BaseModel
from sqlalchemy import select
from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper
from src.shemas.users import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_psw(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = (
            result.scalars().one()
        )  # scalars() берет из каждого кортежа первый элемент
        return UserWithHashedPassword.model_validate(model, from_attributes=True)

