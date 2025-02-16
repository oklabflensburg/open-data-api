from fastapi import Depends, APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from ..dependencies import get_session
from ..services.archaeology import get_archaeological_monument
from ..schemas.archaeology import ArchaeologicalMonumentResponse



route_archaeology = APIRouter(prefix='/archaeology/monument/v1')


@route_archaeology.get(
    '/detail',
    response_model=List[ArchaeologicalMonumentResponse],
    tags=['Denkmalliste unbeweglicher archäologischer Kulturdenkmale'],
)
async def fetch_archaeological_monument(
    monument_id: Optional[int] = Query(None),
    municipality_key: Optional[str] = Query(None),
    object_number: Optional[str] = Query(None),
    date_registered: Optional[str] = Query(None),
    date_modified: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session),
):
    filters = {
        'id': monument_id,
        'municipality_key': municipality_key,
        'object_number': object_number,
        'date_registered': date_registered,
        'date_modified': date_modified,
    }

    # Remove filters with None values
    active_filters = {key: value for key, value in filters.items() if value not in [None, '']}

    if not active_filters:
        raise HTTPException(status_code=400, detail='At least one filter parameter is required')

    rows = await get_archaeological_monument(session, active_filters)

    response = jsonable_encoder(rows)
    return JSONResponse(content=response)
