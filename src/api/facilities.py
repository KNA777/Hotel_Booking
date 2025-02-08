from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.services.facilities import FacilityService
from src.shemas.facilities import FacilityAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение всех удобств")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post("", summary="Добавление удобств")
async def add_facility(db: DBDep, data: FacilityAdd):
    facility = await FacilityService(db).create_facility(data)
    return {"status": True, "data": facility}


# ПРИМЕР ПОДКЛЮЧЕНИЯ И РАБОТЫ С REDIS
# @router.get("", summary="Получение всех удобств")
# async def get_facilities(db: DBDep):
#     facilities_from_cash = await redis_manager.get("facilities")
#     if not facilities_from_cash:
#         facilities = await db.facilities.get_all()
#         facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
#         print(facilities_schemas)
#         facilities_json = json.dumps(facilities_schemas) Конвертация в JSON формат
#         await redis_manager.set("facilities", facilities_json, expire=10)
#         return facilities
#     else:
#         facilities_dict = json.loads(facilities_from_cash)
#         return facilities_dict
