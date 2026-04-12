from typing import List, Optional
from pydantic import BaseModel


class SchoolTypeResponse(BaseModel):
    name: str
    code: int


class GeoPoint(BaseModel):
    type: str = 'Point'
    coordinates: List[float]


class SchoolResponse(BaseModel):
    geojson: Optional[GeoPoint] = None
    id: int
    source_id: Optional[int] = None
    name: str
    city: Optional[str] = None
    zipcode: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    telephone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    agency_number: Optional[str] = None
    main_school_type: Optional[str] = None
    school_types: List[str]
    wikidata_p13491: Optional[str] = None
    wikidata_id: Optional[str] = None
    slug: Optional[str] = None


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
