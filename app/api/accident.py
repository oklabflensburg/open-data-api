from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dependencies import get_session
from ..services.accident import get_accident_meta, get_accident_details_by_city
from ..schemas.accident import DeAccidentMetaResponse

route_accident = APIRouter(prefix='/accident/v1')


@route_accident.get(
    '/meta',
    response_model=List[DeAccidentMetaResponse],
    responses={
        200: {'description': 'OK'},
        400: {'description': 'Bad Request'},
        404: {'description': 'Not Found'},
        422: {'description': 'Unprocessable Entity'},
    },
    tags=['Unfallatlas']
)
async def fetch_accident_meta(session: AsyncSession = Depends(get_session)):
    rows = await get_accident_meta(session)

    if len(rows) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Could not retrieve list of accident meta details'
        )

    return rows


@route_accident.get(
    '/details',
    response_model=List,
    responses={
        200: {'description': 'OK'},
        400: {'description': 'Bad Request'},
        404: {'description': 'Not Found'},
        422: {'description': 'Unprocessable Entity'},
    },
    tags=['Unfallatlas']
)
async def fetch_accident_details_by_city(
    query: str,
    session: AsyncSession = Depends(get_session)
):
    rows = await get_accident_details_by_city(session, query)
    result = jsonable_encoder(rows)

    return JSONResponse(content=result[0])
