from sqlmodel import SQLModel, Field
from typing import Optional
from geoalchemy2 import Geometry
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION


class SHPoliceStation(SQLModel, table=True):
    __tablename__ = "sh_police_station"

    id: int = Field(primary_key=True)
    name: str
    city: str
    zipcode: str = Field(max_length=5)
    street: str
    house_number: str = Field(max_length=10)
    telephone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    longitude: Optional[float] = Field(sa_column=Column(DOUBLE_PRECISION))
    latitude: Optional[float] = Field(sa_column=Column(DOUBLE_PRECISION))
    wkb_geometry: Optional[str] = Field(
        sa_column=Column(Geometry(geometry_type="GEOMETRY", srid=4326))
    )
