from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()



class Monument(Base):
    __tablename__ = 'sh_monuments'

    id = Column(Integer, primary_key=True)
    object_id = Column(String)
    address = Column(String)
    image_url = Column(String)
    designation = Column(String)
    description = Column(String)
    administrative = Column(String)
    monument_type = Column(String)
    postal_code = Column(String)
    place_name = Column(String)
    wkb_geometry = Column(Geometry)
