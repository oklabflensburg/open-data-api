from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP, Date
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()


class DwdStationReference(Base):
    __tablename__ = 'dwd_station_reference'

    id = Column(Integer, primary_key=True)
    station_name = Column(String, nullable=False)
    station_id = Column(String, nullable=False, unique=True)
    identifier = Column(String, nullable=False)
    station_code = Column(String, nullable=False)
    station_latitude = Column(Numeric)
    station_longitude = Column(Numeric)
    station_elevation = Column(Integer)
    river_basin_id = Column(Integer)
    state_name = Column(String, nullable=False)
    recording_start = Column(Date)
    recording_end = Column(Date)
    wkb_geometry = Column(Geometry('POINT', srid=4326))


class WeatherStation(Base):
    __tablename__ = 'de_weather_stations'

    id = Column(Integer, primary_key=True)
    station_id = Column(String, nullable=False, unique=True)
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    station_elevation = Column(Integer)
    latitude = Column(Numeric, nullable=False)
    longitude = Column(Numeric, nullable=False)
    station_name = Column(String)
    state_name = Column(String)
    submission = Column(String)
    wkb_geometry = Column(Geometry('POINT', srid=4326))


class MosmixStation(Base):
    __tablename__ = 'global_mosmix_stations'

    id = Column(Integer, primary_key=True)
    station_id = Column(String, nullable=False, unique=True)
    icao_code = Column(String)
    station_name = Column(String)
    latitude = Column(Numeric, nullable=False)
    longitude = Column(Numeric, nullable=False)
    station_elevation = Column(Integer)
    wkb_geometry = Column(Geometry('POINT', srid=4326))
