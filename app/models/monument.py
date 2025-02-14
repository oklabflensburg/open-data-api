from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from geoalchemy2 import Geometry

Base = declarative_base()



class Monument(Base):
    __tablename__ = 'sh_monument'

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


class ArchaeologicalMonument(Base):
    __tablename__ = 'sh_archaeological_monument'

    id = Column(Integer, primary_key=True, index=True)
    object_name = Column(String, nullable=False)
    proper_name = Column(String, nullable=True)
    object_number = Column(String(50), unique=True, nullable=False)
    district_name = Column(String, nullable=True)
    municipality_name = Column(String, nullable=True)
    object_description = Column(Text, nullable=True)
    object_significance = Column(Text, nullable=True)
    protection_scope = Column(Text, nullable=True)
    date_registered = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    status = Column(String, nullable=True)
    heritage_authority = Column(String, nullable=True)
    municipality_key = Column(String(8), nullable=True)
    wkb_geometry = Column(Geometry('MULTIPOLYGON', srid=4326), nullable=False)
