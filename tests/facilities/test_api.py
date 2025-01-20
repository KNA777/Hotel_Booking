from src.api.facilities import get_facilities
from src.shemas.facilities import FacilityAdd


async def test_get_facilities(ac, db):
    facility_data = FacilityAdd(title="WI-FI")
    new_facility = await db.facilities.add(facility_data)
    get_facility = await db.facilities.get_one_or_none(id=new_facility.id)
    assert new_facility.id == get_facility.id

    response = await ac.get("/facilities")
    assert response.status_code == 200


