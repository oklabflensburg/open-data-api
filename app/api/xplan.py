from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dependencies import get_session
from ..services.xplan import (
    get_plan_by_lat_lng
)

route_xplan = APIRouter(prefix='/xplan/v1')


@route_xplan.get(
    '/point',
    response_model=List,
    responses={
        200: {'description': 'OK'},
        400: {'description': 'Bad Request'},
        404: {'description': 'Not Found'},
        422: {'description': 'Unprocessable Entity'},
    },
    tags=['XPlanung'])
async def fetch_plan_by_lat_lng(
    lat: float,
    lng: float,
    session: AsyncSession = Depends(get_session)
):
    rows = await get_plan_by_lat_lng(session, lat, lng)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not found'
        )