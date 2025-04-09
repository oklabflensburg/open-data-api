from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from sqlmodel import SQLModel, Field
from typing import Optional


Base = declarative_base()


class DistrictNumber(SQLModel, table=True):
    __tablename__ = 'de_district_numbers'
    __table_args__ = {'schema': 'public'}

    id: int = Field(default=None, primary_key=True)
    district_number: Optional[str] = Field(default=None, max_length=5)
    district_name: Optional[str] = None
    notes: Optional[str] = None


class Flurstueck(SQLModel, table=True):
    __tablename__ = 'flurstueck'
    __table_args__ = {'schema': 'public'}

    ogc_fid: int = Field(default=None, primary_key=True)
    identifier: Optional[str] = Field(default=None, max_length=30)
    idflurst: Optional[str] = Field(default=None, max_length=16)
    flstkennz: Optional[str] = Field(default=None, max_length=20)
    land: Optional[str] = Field(default=None, max_length=18)
    landschl: Optional[int] = None
    gemarkung: Optional[str] = Field(default=None, max_length=11)
    gemaschl: Optional[int] = None
    flur: Optional[int] = None
    flurschl: Optional[int] = None
    flstnrzae: Optional[int] = None
    kreis: Optional[str] = Field(default=None, max_length=16)
    kreisschl: Optional[int] = None
    gemeinde: Optional[str] = Field(default=None, max_length=16)
    gmdschl: Optional[int] = None
    oid_: Optional[str] = Field(default=None, max_length=18)
    aktualit: Optional[str] = Field(default=None, max_length=11)
    flaeche: Optional[float] = None
    abwrecht: Optional[str] = Field(default=None, max_length=31)
    lagebeztxt: Optional[str] = Field(default=None, max_length=245)
    flstnrnen: Optional[int] = None
    geometrie: Optional[Geometry] = Field(
        default=None,
        sa_column=Column(
            Geometry('MULTIPOLYGON', srid=4326, spatial_index=True)
        )
    )

    model_config = {
        'arbitrary_types_allowed': True
    }


class MunicipalityKey(SQLModel, table=True):
    __tablename__ = 'de_municipality_keys'
    __table_args__ = {'schema': 'public'}

    id: int = Field(default=None, primary_key=True)
    municipality_key: Optional[str] = Field(default=None, max_length=8)
    municipality_name: Optional[str] = None
    notes: Optional[str] = None


class VG25Gem(SQLModel, table=True):
    __tablename__ = 'vg25_gem'
    __table_args__ = {'schema': 'public'}

    id: int = Field(default=None, primary_key=True)
    objid: Optional[str] = None
    beginn: Optional[datetime] = None
    ade: Optional[int] = None
    gf: Optional[int] = None
    bsg: Optional[int] = None
    ars: Optional[str] = None
    ags: Optional[str] = None
    sdv_ars: Optional[str] = None
    gen: Optional[str] = None
    bez: Optional[str] = None
    ibz: Optional[int] = None
    bem: Optional[str] = None
    nbd: Optional[str] = None
    sn_l: Optional[str] = None
    sn_r: Optional[str] = None
    sn_k: Optional[str] = None
    sn_v1: Optional[str] = None
    sn_v2: Optional[str] = None
    sn_g: Optional[str] = None
    fk_s3: Optional[str] = None
    nuts: Optional[str] = None
    ars_0: Optional[str] = None
    ags_0: Optional[str] = None
    wsk: Optional[datetime] = None
    geom: Optional[Geometry] = Field(
        default=None,
        sa_column=Column(
            Geometry('MULTIPOLYGON', srid=4326, spatial_index=True)
        )
    )

    model_config = {
        'arbitrary_types_allowed': True
    }


class VG25Krs(SQLModel, table=True):
    __tablename__ = "vg25_krs"

    id: int = Field(default=None, primary_key=True)

    objid: Optional[str] = None
    beginn: Optional[datetime] = None
    ade: Optional[int] = None
    gf: Optional[int] = None
    bsg: Optional[int] = None
    ars: Optional[str] = None
    ags: Optional[str] = None
    sdv_ars: Optional[str] = None
    gen: Optional[str] = None
    bez: Optional[str] = None
    ibz: Optional[int] = None
    bem: Optional[str] = None
    nbd: Optional[str] = None
    sn_l: Optional[str] = None
    sn_r: Optional[str] = None
    sn_k: Optional[str] = None
    sn_v1: Optional[str] = None
    sn_v2: Optional[str] = None
    sn_g: Optional[str] = None
    fk_s3: Optional[str] = None
    nuts: Optional[str] = None
    ars_0: Optional[str] = None
    ags_0: Optional[str] = None
    wsk: Optional[datetime] = None

    geom: Optional[Geometry] = Field(
        default=None,
        sa_column=Column(
            Geometry("MULTIPOLYGON", srid=4326, spatial_index=True)
        )
    )

    model_config = {
        "arbitrary_types_allowed": True
    }


class VG25Lan(SQLModel, table=True):
    __tablename__ = "vg25_lan"

    id: int = Field(default=None, primary_key=True)

    objid: Optional[str] = None
    beginn: Optional[datetime] = None
    ade: Optional[int] = None
    gf: Optional[int] = None
    bsg: Optional[int] = None
    ars: Optional[str] = None
    ags: Optional[str] = None
    sdv_ars: Optional[str] = None
    gen: Optional[str] = None
    bez: Optional[str] = None
    ibz: Optional[int] = None
    bem: Optional[str] = None
    nbd: Optional[str] = None
    sn_l: Optional[str] = None
    sn_r: Optional[str] = None
    sn_k: Optional[str] = None
    sn_v1: Optional[str] = None
    sn_v2: Optional[str] = None
    sn_g: Optional[str] = None
    fk_s3: Optional[str] = None
    nuts: Optional[str] = None
    ars_0: Optional[str] = None
    ags_0: Optional[str] = None
    wsk: Optional[datetime] = None

    geom: Optional[Geometry] = Field(
        default=None,
        sa_column=Column(
            Geometry("MULTIPOLYGON", srid=4326, spatial_index=True)
        )
    )

    model_config = {
        "arbitrary_types_allowed": True
    }
