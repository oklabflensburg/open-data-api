import json

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from geojson import Feature, FeatureCollection
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dependencies import get_session
from ..services.monument import (
    get_monument_by_id,
    get_monument_by_slug,
    get_monument_by_object_number,
    get_monument_geometries_by_bbox,
    get_monument_geometries_by_lat_lng
)


route_monument = APIRouter(prefix='/monument/v1')


@route_monument.get(
    '/details',
    response_model=List,
    tags=['Denkmalliste']
)
async def fetch_monument_by_filter(
    monument_id: int = None,
    slug: str = None,
    object_number: str = None,
    session: AsyncSession = Depends(get_session)
):
    filters = [monument_id, slug, object_number]
    if sum(f is not None for f in filters) != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Exactly one argument must be provided'
        )

    if monument_id:
        rows = await get_monument_by_id(session, monument_id)
        identifier = f'monument id {monument_id}'
    elif slug:
        rows = await get_monument_by_slug(session, slug)
        identifier = f'monument slug {slug}'
    else:
        rows = await get_monument_by_object_number(session, object_number)
        identifier = f'monument object_number {object_number}'

    response = jsonable_encoder(rows)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No matches found for {identifier}'
        )

    return JSONResponse(content=response)


@route_monument.get(
    '/bounds',
    response_model=dict,
    tags=['Denkmalliste']
)
async def fetch_monument_geometries_by_bbox(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    session: AsyncSession = Depends(get_session)
):
    rows = await get_monument_geometries_by_bbox(
        session, xmin, ymin, xmax, ymax
    )

    features = [
        Feature(
            id=row['id'],
            geometry=json.loads(row['geom']),
            properties={'label': row['label']},
        )
        for row in rows
    ]

    geojson_data = FeatureCollection(features)
    return JSONResponse(content=jsonable_encoder(geojson_data))


@route_monument.get(
    '/radius',
    response_model=dict,
    tags=['Denkmalliste']
)
async def fetch_monument_geometries_by_lat_lng(
    lat: float,
    lng: float,
    session: AsyncSession = Depends(get_session)
):
    rows = await get_monument_geometries_by_lat_lng(session, lat, lng)

    features = [
        Feature(
            id=row['id'],
            geometry=json.loads(row['geom']),
            properties={'label': row['label']},
        )
        for row in rows
    ]

    geojson_data = FeatureCollection(features)
    return JSONResponse(content=jsonable_encoder(geojson_data))
