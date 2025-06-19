from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl

class GeoPoint(BaseModel):
    type: str = 'Point'
    coordinates: List[float]

class StreetTreeResponse(BaseModel):
    id: int
    tree_number: str
    street: str
    area_type: Optional[str]
    species: str
    north: float
    east: float
    registration_date: str
    type: str
    geom: GeoPoint  # Correctly typed attribute


class CrsProperties(BaseModel):
    name: str


class Crs(BaseModel):
    type: str
    properties: CrsProperties


class TreeFeature(BaseModel):
    type: str = 'Feature'
    id: int
    geometry: GeoPoint


class TreeGeometryResponse(BaseModel):
    type: str = 'FeatureCollection'
    crs: Crs
    features: List[TreeFeature]
