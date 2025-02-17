from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry

Base = declarative_base()



class ArchaeologicalMonument(Base):
    __tablename__ = 'sh_archaeological_monument'

    id = Column(Integer, primary_key=True, index=True)
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
    categories = relationship(
        'ArchaeologicalMonumentCategory',
        secondary='sh_archaeological_monument_x_category',
        back_populates='monuments'
    )


class ArchaeologicalMonumentCategory(Base):
    __tablename__ = 'sh_archaeological_monument_category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String, unique=True, nullable=False)

    monuments = relationship(
        'ArchaeologicalMonument',
        secondary='sh_archaeological_monument_x_category',
        back_populates='categories'
    )


class ArchaeologicalMonumentXCategory(Base):
    __tablename__ = 'sh_archaeological_monument_x_category'

    category_id = Column(Integer, ForeignKey('sh_archaeological_monument_category.id'), primary_key=True)
    monument_id = Column(Integer, ForeignKey('sh_archaeological_monument.id'), primary_key=True)
