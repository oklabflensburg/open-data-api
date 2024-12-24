from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dependencies import get_session
from ..service import get_accident_meta, get_accident_details_by_city

route_accident = APIRouter(prefix='/accident/v1')


@route_accident.get(
    '/meta',
    response_model=List,
    tags=['Unfallatlas']
)
async def fetch_accident_meta(session: AsyncSession = Depends(get_session)):
    rows = await get_accident_meta(session)
    result = jsonable_encoder(rows)

    return JSONResponse(content=result[0])


@route_accident.get(
    '/details',
    response_model=List,
    tags=['Unfallatlas']
)
async def fetch_accident_details_by_city(query: str, session: AsyncSession = Depends(get_session)):
    rows = await get_accident_details_by_city(session, query)
    result = jsonable_encoder(rows)

    return JSONResponse(content=result[0])
