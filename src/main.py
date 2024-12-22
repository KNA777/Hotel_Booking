import sys
import uvicorn
from fastapi import FastAPI
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotel_router
from src.api.auth import router as auth_router
from src.api.rooms import router as room_router
from src.api.bookings import router as room_booking
from src.api.facilities import router as facility_router

app = FastAPI(summary="Бронирование Отелей")

app.include_router(auth_router)
app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(facility_router)
app.include_router(room_booking)




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
