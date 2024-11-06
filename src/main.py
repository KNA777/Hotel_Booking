from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotel_router

app = FastAPI(summary="Бронирование Отелей")

app.include_router(hotel_router)




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
