from sqlalchemy import select, delete, insert

from src.models.facilities import FacilitiesOrm, FacilitiesRoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper
from src.shemas.facilities import RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class FacilitiesRoomsRepository(BaseRepository):
    model = FacilitiesRoomsOrm
    schema = RoomFacility

    async def set_new_facilities_rooms(
        self, room_id: int, facility_ids: list[int]
    ) -> None:
        ids_facility_in_m2m_table = select(self.model.facility_id).filter_by(
            room_id=room_id
        )

        res = await self.session.execute(ids_facility_in_m2m_table)
        current_ids_facilities = res.scalars().all()  # [1,2,3] список id удобств
        ids_to_delete = list(set(current_ids_facilities) - set(facility_ids))
        ids_to_insert = list(set(facility_ids) - set(current_ids_facilities))

        if ids_to_delete:
            delete_m2m_facilities = delete(self.model).filter(
                self.model.room_id == room_id, self.model.facility_id.in_(ids_to_delete)
            )
            await self.session.execute(delete_m2m_facilities)

        if ids_to_insert:
            insert_m2m_facilities = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert]
            )

            await self.session.execute(insert_m2m_facilities)
