from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dependencies import get_session
from ..services.monument import get_monument_by_object_id


route_monument = APIRouter(prefix='/monument/v1')


@route_monument.get(
    '/details',
    response_model=List, tags=['Denkmalliste'])
async def fetch_monument_by_object_id(object_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_monument_by_object_id(session, object_id)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No matches found for object id {object_id}')

    return JSONResponse(content=response)

