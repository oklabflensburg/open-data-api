from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dependencies import get_session
from ..service import get_biotope_meta_by_lat_lng, get_biotope_origin_meta

route_biotope = APIRouter(prefix='/biotope/v1')


@route_biotope.get(
    '/point',
    response_model=list, tags=['Biotopkartierung'])
async def fetch_biotope_meta_by_lat_lng(lat: float, lng: float, session: AsyncSession = Depends(get_session)):
    rows = await get_biotope_meta_by_lat_lng(session, lat, lng)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Not found')


@route_biotope.get(
    '/origin',
    response_model=list, tags=['Biotopkartierung'])
async def fetch_biotope_origin(code: str, session: AsyncSession = Depends(get_session)):
    rows = await get_biotope_origin_meta(session, code)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Not found')

