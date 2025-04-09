from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl


class SchoolTypeResponse(BaseModel):
    name: str
    code: int


class GeoPoint(BaseModel):
    type: str = 'Point'
    coordinates: List[float]


class SchoolResponse(BaseModel):
    geojson: GeoPoint
    id: int
    name: str
    city: str
    zipcode: str
    street: str
    house_number: str
    telephone: str
    fax: Optional[str] = None
    email: EmailStr
    website: Optional[HttpUrl] = None
    agency_number: str
    main_school_type: str
    school_types: List[str]
    slug: str


class CrsProperties(BaseModel):
    name: str


class Crs(BaseModel):
    type: str
    properties: CrsProperties


class SchoolProperties(BaseModel):
    label: str
    school_type: Optional[int] = None


class SchoolFeature(BaseModel):
    type: str = 'Feature'
    id: int
    geometry: GeoPoint
    properties: SchoolProperties


class SchoolGeometryResponse(BaseModel):
    type: str = 'FeatureCollection'
    crs: Crs
    features: List[SchoolFeature]
