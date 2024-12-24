from fastapi import Depends, APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dependencies import get_session
from ..services.climate import get_dwd_stations_by_municipality_key, get_weather_service_stations
from ..schemas.climate import DwdStationReferenceResponse, WeatherStationResponse


route_climate = APIRouter(prefix='/climate/v1')


@route_climate.get(
    '/stations/list',
    response_model=List[DwdStationReferenceResponse],
    tags=['Deutscher Wetterdienst'],
    description=('Retrieves a list of German weather service stations reference with corresponding ids.')
)
async def fetch_dwd_stations_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_dwd_stations_by_municipality_key(session, municipality_key)

    if len(rows) == 0:
        raise HTTPException(status_code=404, detail='Could not retrieve list of German weather service stations reference')

    return rows



@route_climate.get(
    '/list',
    response_model=List[WeatherStationResponse],
    tags=['Deutscher Wetterdienst'],
    description=('Retrieves a list of German weather service stations with corresponding ids.')
)
async def fetch_weather_stations(session: AsyncSession = Depends(get_session)):
    rows = await get_weather_service_stations(session)

    if len(rows) == 0:
        raise HTTPException(status_code=404, detail='Could not retrieve list of German weather service stations')

    return rows


