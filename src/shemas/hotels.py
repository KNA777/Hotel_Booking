from pydantic import BaseModel


class Hotel(BaseModel):
    title: str
    address: str

class HotelPatch(BaseModel):
    title: str | None = None
    address: str | None = None