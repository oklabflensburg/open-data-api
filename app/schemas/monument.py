from pydantic import BaseModel
from typing import Optional



class ArchaeologicalMonumentResponse(BaseModel):
    monument_id: int
    object_name: str
    proper_name: Optional[str] = None
    object_number: str
    district_name: Optional[str] = None
    municipality_name: Optional[str] = None
    object_description: Optional[str] = None
    object_significance: Optional[str] = None
    protection_scope: Optional[str] = None
    date_registered: Optional[str] = None
    date_modified: Optional[str] = None
    status: Optional[str] = None
    heritage_authority: Optional[str] = None
    municipality_key: Optional[str] = None
    geojson: Optional[dict] = None
