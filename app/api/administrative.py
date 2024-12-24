from fastapi import Depends, APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dependencies import get_session
from ..services.administrative import get_parcel_meta_by_lat_lng, get_municipality_by_query, get_municipality_by_name, get_municipality_by_key


route_administrative = APIRouter(prefix='/administrative/v1')


@route_administrative.get(
    '/parcel',
    response_model=List, tags=['Verwaltungsgebiete'])
async def fetch_parcel_meta_by_lat_lng(lat: float, lng: float, session: AsyncSession = Depends(get_session)):
    rows = await get_parcel_meta_by_lat_lng(session, lat, lng)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Not found')


@route_administrative.get(
    '/municipality/search',
    response_model=List,
    tags=['Verwaltungsgebiete'],
    description=('Retrieves municipality name and key as well as the region name based on the provided query.')
)
async def fetch_municipality_by_query(
    query: str = Query(None, min_length=2),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_municipality_by_query(session, query)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'no results found')


@route_administrative.get(
    '/municipality',
    response_model=List,
    tags=['Verwaltungsgebiete'],
    description=('Retrieves the geometry, bounding box, shape area, and statistical information of a municipality based on the provided municipality key (AGS) or the municipality name.')
)
async def fetch_municipality(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    municipality_name: str = Query(None, min_length=2),
    session: AsyncSession = Depends(get_session)
):
    if municipality_key:
        rows = await get_municipality_by_key(session, municipality_key)
        response = jsonable_encoder(rows)

        if len(response) == 0:
            raise HTTPException(status_code=404, detail='No municipality was found')

        return JSONResponse(content=response)
    elif municipality_name:
        rows = await get_municipality_by_name(session, municipality_name)
        response = jsonable_encoder(rows)

        if len(response) == 0:
            raise HTTPException(status_code=404, detail='No municipality was found')

        return JSONResponse(content=response)
    else:
        raise HTTPException(status_code=400, detail='Either "key" or "name" parameter must be provided')

