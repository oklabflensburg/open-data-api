from fastapi import Depends, APIRouter, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from geojson import Feature, FeatureCollection

from ..dependencies import get_session
from ..services.climate import (
    get_dwd_stations_by_municipality_key,
    get_mosmix_nearest_geometriey_by_position,
    get_mosmix_geometries_by_radius,
    get_mosmix_geometries_by_bbox,
    get_weather_service_stations,
    get_all_mosmix_stations
)

from ..schemas.climate import (
    DwdStationReferenceResponse,
    WeatherStationResponse,
    MosmixStationResponse
)

from ..utils.dwd_kmz import retrieve_station_kmz


route_climate = APIRouter(prefix='/climate/v1')


@route_climate.get(
    '/stations/list',
    response_model=List[DwdStationReferenceResponse],
    responses={
        200: {'description': 'OK'},
        400: {'description': 'Bad Request'},
        404: {'description': 'Not Found'},
        422: {'description': 'Unprocessable Entity'},
    },
    tags=['Deutscher Wetterdienst'],
    description=(
        'Retrieves a list of German weather service stations reference with corresponding ids.'
    )
)
async def fetch_dwd_stations_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_dwd_stations_by_municipality_key(
        session,
        municipality_key
    )

    if len(rows) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Could not retrieve list of German weather service stations reference'
        )

    return rows


@route_climate.get(
    '/list',
    response_model=List[WeatherStationResponse],
    responses={
        200: {'description': 'OK'},
        400: {'description': 'Bad Request'},
        404: {'description': 'Not Found'},
        422: {'description': 'Unprocessable Entity'},
    },
    tags=['Deutscher Wetterdienst'],
    description=(
        'Retrieves a list of German weather service stations with corresponding ids.'
    )
)
async def fetch_weather_stations(session: AsyncSession = Depends(get_session)):
    rows = await get_weather_service_stations(session)

    if len(rows) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Could not retrieve list of German weather service stations'
        )

    return rows


@route_climate.get(
    '/mosmix/list',
    response_model=List[MosmixStationResponse],
    responses={
        200: {'description': 'OK'},
        400: {'description': 'Bad Request'},
        404: {'description': 'Not Found'},
        422: {'description': 'Unprocessable Entity'},
    },
    tags=['Deutscher Wetterdienst'],
    description=(
        'Retrieves a list of global MOSMIX stations with corresponding ids.'
    )
)
async def fetch_mosmix_stations(session: AsyncSession = Depends(get_session)):
    rows = await get_all_mosmix_stations(session)

    if len(rows) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Could not retrieve list of German weather service stations'
        )

    return rows


@route_climate.get(
    '/mosmix/bounds',
    response_model=dict,
    tags=['Deutscher Wetterdienst'],
    description=(
        'Retrieves a list of German weather service stations within the '
        'specified bounding box.'
    ),
    responses={
        200: {'description': 'OK'},
        400: {'description': 'Bad Request'},
        404: {'description': 'Not Found'},
        422: {'description': 'Unprocessable Entity'},
    }
)
async def fetch_mosmix_geometries_by_bbox(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    session: AsyncSession = Depends(get_session)
):
    rows = await get_mosmix_geometries_by_bbox(
        session, xmin, ymin, xmax, ymax
    )

    if len(rows) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No matches found for the given bounding box'
        )

    features = [
        Feature(
            id=row['station_id'],
            geometry=row['geojson'],
            properties={'station_name': row['station_name']},
        )
        for row in rows
    ]

    crs = {'type': 'name', 'properties': {
        'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'}}
    geojson_data = FeatureCollection(features, crs=crs)

    return geojson_data


@route_climate.get(
    '/mosmix/radius',
    response_model=dict,
    tags=['Deutscher Wetterdienst'],
    description=(
        'Retrieves a list of German weather service stations within the '
        'specified radius.'
    ),
    responses={
        200: {'description': 'OK'},
        400: {'description': 'Bad Request'},
        404: {'description': 'Not Found'},
        422: {'description': 'Unprocessable Entity'},
    }
)
async def fetch_mosmix_geometries_by_radius(
    lat: float,
    lng: float,
    radius: float = Query(
        default=5000,
        ge=0,
        le=100000,
        description='Radius in meters'
    ),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_mosmix_geometries_by_radius(session, lat, lng, radius)

    if len(rows) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No matches found for coordinates ({lat}, {lng})'
        )

    features = [
        Feature(
            id=row['station_id'],
            geometry=row['geojson'],
            properties={'station_name': row['station_name']},
        )
        for row in rows
    ]

    crs = {'type': 'name', 'properties': {
        'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'}}
    geojson_data = FeatureCollection(features, crs=crs)

    return geojson_data


@route_climate.get(
    '/mosmix/nearest',
    response_model=dict,
    tags=['Deutscher Wetterdienst'],
    description=(
        'Retrieves the nearest of German weather service station'
        ' to the specified coordinates.'),
    responses={
        200: {'description': 'OK'},
        400: {'description': 'Bad Request'},
        404: {'description': 'Not Found'},
        422: {'description': 'Unprocessable Entity'},
    }
)
async def fetch_mosmix_nearest_geometriey_by_position(
    lat: float,
    lng: float,
    session: AsyncSession = Depends(get_session)
):
    row = await get_mosmix_nearest_geometriey_by_position(
        session, lat, lng
    )

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No matches found for coordinates ({lat}, {lng})'
        )

    feature = Feature(
        id=row['station_id'],
        geometry=row['geojson'],
        properties={'station_name': row['station_name']},
    )

    crs = {'type': 'name', 'properties': {
        'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'}}
    geojson_data = FeatureCollection([feature], crs=crs)

    return geojson_data


@route_climate.get(
    '/mosmix/forecast/{station_id}',
    response_model=dict,
    tags=['Deutscher Wetterdienst'],
    description=(
        'Retrieves a KML file for the specified station ID.'
    ),
    responses={
        200: {'description': 'OK'},
        400: {'description': 'Bad Request'},
        404: {'description': 'Not Found'},
        422: {'description': 'Unprocessable Entity'},
    }
)
async def fetch_forecast_station_kmz(
    station_id: int
):
    data = await retrieve_station_kmz(station_id)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No matches found for station ID {station_id}'
        )

    return data
