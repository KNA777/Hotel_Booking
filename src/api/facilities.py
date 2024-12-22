from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.shemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.post("", summary="Добавление удобств")
async def add_facility(db: DBDep, data: FacilityAdd):
    await db.facilities.add(data)
    await db.commit()
    return {"status": True}


@router.get("", summary="Получение всех удобств")
async def get_facilities(db: DBDep):
    facilities = await db.facilities.get_all()
    return {"data": facilities}
