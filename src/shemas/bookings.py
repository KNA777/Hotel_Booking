from datetime import date
from pydantic import BaseModel


class BookingsRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class Bookings(BookingsRequest):
    id: int
    user_id: int
    price: int


class BookingsAdd(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
