from fastapi import FastAPI, Query, Path
import uvicorn

app = FastAPI()

hotels = [

    {"id": 1, "title": "Sochi"},
    {"id": 2, "title": "Tver"}

]

@app.get("/hotels")
def get_all_hotels(
        id: int | None = Query(None, description="Идентификационный ключ отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    return hotels_

@app.post("/hotels")
def add_hotel(
        title: str
):
    global hotels
    new_hotel = {
        "id": hotels[-1]["id"] + 1,
        "title": title
    }
    hotels.append(new_hotel)
    return hotels

@app.delete("/hotels/{hotel_id}")
async def delete_hotel(
        hotel_id: int = Path(description="Идентификационный ключ отеля")
):
    global hotels
    # hotels_ = []
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {
        "status": "OK",
        "all_hotels": hotels
    }



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

