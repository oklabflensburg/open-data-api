import json

from typing import List, Dict, Any, Optional

from fastapi import Depends, APIRouter, HTTPException, status
from geojson import Feature, FeatureCollection
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.police import (
    PoliceGeometryResponse,
    PoliceResponse
)
from ..dependencies import get_session
from ..services.police import (
    get_police_station_by_id,
    get_police_station_geometries_by_bbox,
    get_police_station_geometries_by_lat_lng
)


route_police = APIRouter(prefix='/police/v1')


def create_geojson_from_rows(rows: List[Dict[str, Any]]) -> FeatureCollection:
    features = [
        Feature(
            id=row['id'],
            geometry=json.loads(row['geojson']),
            properties={'label': row['label']}
        )
        for row in rows
    ]

    crs = {'type': 'name', 'properties': {
        'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'}}

    return FeatureCollection(features, crs=crs)


@route_police.get(
    '/details',
    response_model=PoliceResponse,
    tags=['Polizeidienststellen'],
    description=(
        'Retrieves police station details based on the provided station id.'
    )
)
async def fetch_police_station_by_id(
    station_id: int,
    session: AsyncSession = Depends(get_session)
) -> List[PoliceResponse]:
    rows = await get_police_station_by_id(session, station_id)
    identifier = f'station_id {station_id}'

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No matches found for {identifier}'
        )

    return rows


@route_police.get(
    '/bounds',
    response_model=PoliceGeometryResponse,
    tags=['Polizeidienststellen'],
    description=(
        'Retrieves police geometries based on the provided bounding box. '
        'The coordinates must be in the order: xmin, ymin, xmax, ymax.'
    )
)
async def fetch_police_station_geometries_by_bbox(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    session: AsyncSession = Depends(get_session)
) -> FeatureCollection:
    rows = await get_police_station_geometries_by_bbox(
        session, xmin, ymin, xmax, ymax
    )

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No matches found for the given bounding box'
        )

    return create_geojson_from_rows(rows)


@route_police.get(
    '/radius',
    response_model=PoliceGeometryResponse,
    responses={
        400: {
            'description': 'Bad Request',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'string'
                    }
                }
            }
        },
        404: {
            'description': 'Not Found',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'string'
                    }
                }
            }
        },
        422: {
            'description': 'Unprocessable Entity',
            'content': {
                'application/json': {
                    'example': {
                        'detail': [
                            {
                                'loc': ['query', 'station_id'],
                                'msg': 'value is not a valid integer',
                                'type': 'type_error.integer'
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=['Polizeidienststellen'],
    description=(
        'Retrieves police geometries based on the provided latitude and longitude. '
        'The coordinates must be in the order: lat, lng.'
    )
)
async def fetch_police_station_geometries_by_lat_lng(
    lat: float,
    lng: float,
    session: AsyncSession = Depends(get_session)
) -> FeatureCollection:
    """
    Retrieve polices near a specific lat/lng point.

    Args:
        lat: Latitude
        lng: Longitude
        session: Database session

    Returns:
        GeoJSON FeatureCollection of polices

    Raises:
        HTTPException: If no polices are found near the coordinates
    """
    rows = await get_police_station_geometries_by_lat_lng(session, lat, lng)

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No matches found for coordinates ({lat}, {lng})'
        )

    return create_geojson_from_rows(rows)
