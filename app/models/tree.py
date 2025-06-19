from sqlmodel import SQLModel, Field
from geoalchemy2 import Geometry
from sqlalchemy import Column, Numeric, String, Date
from typing import Optional
import datetime

class StreetTreeRegister(SQLModel, table=True):
    __tablename__ = "street_tree_register"
    __table_args__ = {'schema': 'flensburg'}

    id: int = Field(primary_key=True)  # nullable=False implied for primary_key
    tree_number: str = Field(nullable=False)  # simple field, no sa_column so nullable allowed here
    street: str = Field(sa_column=Column(String, nullable=False))
    area_type: Optional[str] = Field(sa_column=Column(String, nullable=True), default=None)
    species: str = Field(sa_column=Column(String, nullable=False))
    north: float = Field(sa_column=Column(Numeric, nullable=False))
    east: float = Field(sa_column=Column(Numeric, nullable=False))
    registration_date: datetime.date = Field(sa_column=Column(Date(), nullable=False))
    type: str = Field(sa_column=Column(String, nullable=False))
    geom: object = Field(sa_column=Column(Geometry('POINT', srid=31467), nullable=True))  # nullable depends on DB column