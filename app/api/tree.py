import json

from typing import List, Dict, Any, Optional

from fastapi import Depends, APIRouter, HTTPException, status
from geojson import Feature, FeatureCollection
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.tree import (
    TreeGeometryResponse,
    TreeResponse
)
from ..dependencies import get_session
from ..services.tree import (
    get_tree_by_id
)

route_police = APIRouter(prefix='/tree/v1')

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
    response_model=TreeResponse,
    tags=['Polizeidienststellen'],
    description=(
        'Retrieves police station details based on the provided station id.'
    )
)
async def fetch_tree_by_id(
    tree_id: int,
    session: AsyncSession = Depends(get_session)
) -> List[TreeResponse]:
    rows = await get_tree_by_id(session, tree_id)
    identifier = f'station_id {tree_id}'

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No matches found for {identifier}'
        )

    return rows
