from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.shemas.rooms import Rooms, RoomsWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_rooms_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date
    ):
        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomsWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]