import sqlalchemy
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by))
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    # from_attributes=True это чтобы pydantic схема смогла перевести объект SQLAlchemy в pydantic объект
    # благодаря этому параметру pydantic может брать атрибуты других классов(HotelsOrm)

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()  # scalars() берет из каждого кортежа первый элемент
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(stmt)
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=401, detail="Введены неправильные данные")
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]):
        if data:
            stmt = insert(self.model).values([item.model_dump() for item in data])
            await self.session.execute(stmt)


    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(stmt)

    # exclude_unset=True - те поля которые не изменялись, не будут записываться как null в таблицу

    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)

