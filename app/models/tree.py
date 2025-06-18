from sqlmodel import SQLModel, Field
from geoalchemy2 import Geometry
from sqlalchemy import Column, Numeric, String, Date


class Street_tree_register(SQLModel, table=True):
    __tablename__ = "flensburg.street_tree_register"

    id: int = Field(primary_key=True, nullable=False)
    tree_number = Column(String, nullable=False)
    street = Column(String, nullable=False)
    area_type = Column(String)
    species = Column(String, nullable=False)
    north = Column(Numeric, nullable=False)
    east = Column(Numeric, nullable=False)
    register_date = Column(Date, nullable=False)
    type = Column(String, nullable=False)
    geom = Column(Geometry('POINT', srid=4326))
