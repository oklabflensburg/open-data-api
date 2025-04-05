from fastapi import Depends, APIRouter, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dependencies import get_session
from ..services.climate import (
    get_dwd_stations_by_municipality_key,
    get_weather_service_stations,
    get_all_mosmix_stations
)

from ..schemas.climate import (
    DwdStationReferenceResponse,
    WeatherStationResponse,
    MosmixStationResponse
)


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