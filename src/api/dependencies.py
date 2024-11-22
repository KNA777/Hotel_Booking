from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Номер страницы", ge=1)]
    per_page: Annotated[int | None, Query(3, description="Количество отелей на странице", ge=1, lt=20)]


PaginationDep = Annotated[PaginationParams, Depends()]


