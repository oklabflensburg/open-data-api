from sqlalchemy import Column, Integer, SmallInteger, Numeric, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()



class Vg250Gem(Base):
    __tablename__ = 'vg250_gem'

    id = Column(Integer, primary_key=True, nullable=False)
    objid = Column(String)
    beginn = Column(TIMESTAMP(timezone=True))
    ade = Column(SmallInteger)
    gf = Column(SmallInteger)
    bsg = Column(SmallInteger)
    ars = Column(String)
    ags = Column(String)
    sdv_ars = Column(String)
    gen = Column(String)
    bez = Column(String)
    ibz = Column(SmallInteger)
    bem = Column(String)
    nbd = Column(String)
    sn_l = Column(String)
    sn_r = Column(String)
    sn_k = Column(String)
    sn_v1 = Column(String)
    sn_v2 = Column(String)
    sn_g = Column(String)
    fk_s3 = Column(String)
    nuts = Column(String)
    ars_0 = Column(String)
    ags_0 = Column(String)
    wsk = Column(TIMESTAMP(timezone=True))
    ewz = Column(Integer)
    kfl = Column(Numeric)
    dlm_id = Column(String)
    geom = Column(Geometry('MULTIPOLYGON', srid=4326))
