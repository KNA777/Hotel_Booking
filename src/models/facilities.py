import typing
from src.database import BaseOrm
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

if typing.TYPE_CHECKING:
    from src.models import RoomsOrm


class FacilitiesOrm(BaseOrm):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(25))

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="facilities", secondary="facilities_rooms"
    )


class FacilitiesRoomsOrm(BaseOrm):
    __tablename__ = "facilities_rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
