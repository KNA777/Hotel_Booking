from src.services.base import BaseService
from src.shemas.facilities import FacilityAdd
from src.tasks.tasks import test_task

class FacilityService(BaseService):

    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def create_facility(self, data: FacilityAdd):
        facility = await self.db.facilities.add(data)
        test_task.delay()
        await self.db.commit()
        return facility
