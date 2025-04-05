from pydantic import BaseModel
from typing import Optional


class DwdStationReferenceResponse(BaseModel):
    station_name: str
    station_id: str
    identifier: str
    station_code: str
    station_elevation: Optional[int] = None
    river_basin_id: Optional[int] = None
    state_name: str
    recording_start: Optional[str] = None
    recording_end: Optional[str] = None
    geojson: Optional[dict] = None


class WeatherStationResponse(BaseModel):
    station_id: str
    start_date: str
    end_date: str
    station_elevation: Optional[int]
    station_name: Optional[str]
    state_name: Optional[str]
    submission: Optional[str]
    geojson: dict


class MosmixStationResponse(BaseModel):
    station_id: str
    icao_code: Optional[str] = None
    station_name: Optional[str] = None
    station_elevation: Optional[int]
    geojson: Optional[dict] = None
