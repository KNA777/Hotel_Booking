import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from pathlib import Path

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

from src.init_redis import redis_manager
from src.api.hotels import router as hotel_router
from src.api.auth import router as auth_router
from src.api.rooms import router as room_router
from src.api.bookings import router as room_booking
from src.api.facilities import router as facility_router
from src.api.images import router as image_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()


app = FastAPI(summary="Бронирование Отелей", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(facility_router)
app.include_router(room_booking)
app.include_router(image_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)
