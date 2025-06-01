from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl


class GeoPoint(BaseModel):
    type: str = 'Point'
    coordinates: List[float]


class PoliceResponse(BaseModel):
    id: int
    name: str
    city: str
    zipcode: str
    street: str
    house_number: str
    telephone: str
    fax: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[HttpUrl] = None
    geojson: Optional[GeoPoint] = None


class CrsProperties(BaseModel):
    name: str


class Crs(BaseModel):
    type: str
    properties: CrsProperties


class PoliceProperties(BaseModel):
    label: str


class PoliceFeature(BaseModel):
    type: str = 'Feature'
    id: int
    geometry: GeoPoint
    properties: PoliceProperties


class PoliceGeometryResponse(BaseModel):
    type: str = 'FeatureCollection'
    crs: Crs
    features: List[PoliceFeature]
