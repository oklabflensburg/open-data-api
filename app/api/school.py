import json

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from geojson import Feature, FeatureCollection
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dependencies import get_session
from ..services.school import (
    get_school_by_id,
    get_school_by_slug,
    get_school_geometries_by_bbox,
    get_school_geometries_by_lat_lng
)


route_school = APIRouter(prefix='/school/v1')


@route_school.get(
    '/details',
    response_model=List,
    tags=['Schulen']
)
async def fetch_school_by_filter(
    school_id: int = None,
    slug: str = None,
    session: AsyncSession = Depends(get_session)
):
    filters = [school_id, slug]
    if sum(f is not None for f in filters) != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Exactly one argument must be provided'
        )

    if school_id:
        rows = await get_school_by_id(session, school_id)
        identifier = f'school id {school_id}'
    else:
        rows = await get_school_by_slug(session, slug)
        identifier = f'school slug {slug}'

    response = jsonable_encoder(rows)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No matches found for {identifier}'
        )

    return JSONResponse(content=response)


@route_school.get(
    '/bounds',
    response_model=dict,
    tags=['Schulen']
)
async def fetch_school_geometries_by_bbox(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    session: AsyncSession = Depends(get_session)
):
    rows = await get_school_geometries_by_bbox(
        session, xmin, ymin, xmax, ymax
    )

    features = [
        Feature(
            id=row['id'],
            geometry=json.loads(row['wkb_geometry']),
            properties={'label': row['label']},
        )
        for row in rows
    ]

    geojson_data = FeatureCollection(features)
    return JSONResponse(content=jsonable_encoder(geojson_data))


@route_school.get(
    '/radius',
    response_model=dict,
    tags=['Schulen']
)
async def fetch_school_geometries_by_lat_lng(
    lat: float,
    lng: float,
    session: AsyncSession = Depends(get_session)
):
    rows = await get_school_geometries_by_lat_lng(session, lat, lng)

    features = [
        Feature(
            id=row['id'],
            geometry=json.loads(row['wkb_geometry']),
            properties={'label': row['label']},
        )
        for row in rows
    ]

    geojson_data = FeatureCollection(features)
    return JSONResponse(content=jsonable_encoder(geojson_data))
