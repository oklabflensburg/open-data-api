import json
import topojson as tp

from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from geojson import Feature, FeatureCollection, Point
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dependencies import get_session
from ..services.monument import get_monument_by_object_id, get_monument_geometries_by_bbox


route_monument = APIRouter(prefix='/monument/v1')


@route_monument.get(
    '/details',
    response_model=List,
    tags=['Denkmalliste']
)
async def fetch_monument_by_object_id(object_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_monument_by_object_id(session, object_id)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No matches found for object id {object_id}')

    return JSONResponse(content=response)



@route_monument.get(
    '/geometries',
    response_model=dict,
    tags=['Denkmalliste']
)
async def fetch_monument_geometries_by_bbox(xmin: float, ymin: float, xmax: float, ymax: float, session: AsyncSession = Depends(get_session)):
    rows = await get_monument_geometries_by_bbox(session, xmin, ymin, xmax, ymax)
    features = [
        Feature(
            id=row['id'],
            geometry=json.loads(row['geom']),
            properties={'label': f'{row["street"]} {row["housenumber"] or None}'}
        )
        for row in rows
    ]
    
    geojson_data = FeatureCollection(features)
    topojson_data = tp.Topology(geojson_data).to_dict()
    print(topojson_data)
    response = jsonable_encoder(topojson_data)

    return JSONResponse(content=response)
