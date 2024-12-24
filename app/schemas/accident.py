from pydantic import BaseModel



class DeAccidentMetaResponse(BaseModel):
    value: int
    name: str
    category: str
