import json

from typing import List, Dict, Any

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from geojson import Feature, FeatureCollection
from sqlalchemy.ext.asyncio import AsyncSession



from ..schemas.tree import (
    StreetTreeResponse
)
from ..dependencies import get_session
from ..services.tree import (
    get_tree_by_id,
    get_tree_by_species
)

from geoalchemy2.shape import to_shape
from shapely.geometry import mapping

route_street_tree = APIRouter(prefix='/street_tree/v1')

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


@route_street_tree.get(
    '/details',
    response_model=StreetTreeResponse,
    responses={
        200: {'description': 'OK'},
        400: {'description': 'Bad Request'},
        404: {'description': 'Not Found'},
        422: {'description': 'Unprocessable Entity'},
        500: {'description': 'Internal Server Error'}
    },
    tags=['Strassenbaeume'],
    description='Retrieves street tree details based on the provided tree id.'
)
async def fetch_tree_by_id(
    tree_id: int,
    session: AsyncSession = Depends(get_session)
) -> StreetTreeResponse:
    row = await get_tree_by_id(session, tree_id)

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No matches found for tree_id {tree_id}'
        )

    # `row` is a RowMapping, convert to model instance or dict if needed
    tree: StreetTreeRegister = row[0] if isinstance(row, tuple) else row

    # Convert WKBElement geom to GeoJSON dict
    shape = to_shape(tree.geom)
    geojson_dict = mapping(shape)

    # Return tree data with geom as GeoJSON dict
    return {
        "id": tree.id,
        "tree_number": tree.tree_number,
        "street": tree.street,
        "area_type": tree.area_type,
        "species": tree.species,
        "north": tree.north,
        "east": tree.east,
        "registration_date": tree.registration_date.isoformat() if tree.registration_date else None,
        "type": tree.type,
        "geom": geojson_dict,
    }

@route_street_tree.get(
    '/species',
    response_model=List,
    tags=['Strassenbaeume'],
    description='Retrieves street tree details based there species.'
)
async def fetch_tree_by_species(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_tree_by_species(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not found'
        )
