import json

from typing import List, Dict, Any, Optional

from fastapi import Depends, APIRouter, HTTPException, status
from geojson import Feature, FeatureCollection
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.school import (
    SchoolGeometryResponse,
    SchoolTypeResponse,
    SchoolResponse
)
from ..dependencies import get_session
from ..services.school import (
    get_school_by_id,
    get_school_by_slug,
    get_school_types,
    get_school_geometries_by_bbox,
    get_school_geometries_by_lat_lng,
    get_school_geometries_by_school_type
)


route_school = APIRouter(prefix='/school/v1')


def create_geojson_from_rows(rows: List[Dict[str, Any]]) -> FeatureCollection:
    """
    Create a GeoJSON FeatureCollection from database rows.

    Args:
        rows: List of database rows containing geojson, id, label and school_type

    Returns:
        A GeoJSON FeatureCollection
    """
    features = [
        Feature(
            id=row['id'],
            geometry=json.loads(row['geojson']),
            properties={'label': row['label'],
                        'school_type': row['school_type']},
        )
        for row in rows
    ]

    crs = {'type': 'name', 'properties': {
        'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'}}

    return FeatureCollection(features, crs=crs)


@route_school.get(
    '/details',
    response_model=List[SchoolResponse],
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
                                'loc': ['query', 'school_id'],
                                'msg': 'value is not a valid integer',
                                'type': 'type_error.integer'
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=['Schulen'],
    description=(
        'Retrieves school details based on the provided filter. '
        'Exactly one of the following arguments must be provided: '
        'school_id, slug.'
    )
)
async def fetch_school_by_filter(
    school_id: Optional[int] = None,
    slug: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
) -> List[SchoolResponse]:
    """
    Retrieve school details by either ID or slug.

    Args:
        school_id: The school ID to lookup
        slug: The school slug to lookup
        session: Database session

    Returns:
        List of school details

    Raises:
        HTTPException: If no filter is provided or no school is found
    """
    filters = [school_id, slug]
    if sum(f is not None for f in filters) != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Exactly one argument must be provided'
        )

    if school_id:
        rows = await get_school_by_id(session, school_id)
        identifier = f'school id {school_id}'
    else:
        rows = await get_school_by_slug(session, slug)
        identifier = f'school slug {slug}'

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No matches found for {identifier}'
        )

    return rows


@route_school.get(
    '/bounds',
    response_model=SchoolGeometryResponse,
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
                                'loc': ['query', 'school_id'],
                                'msg': 'value is not a valid integer',
                                'type': 'type_error.integer'
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=['Schulen'],
    description=(
        'Retrieves school geometries based on the provided bounding box. '
        'The coordinates must be in the order: xmin, ymin, xmax, ymax.'
    )
)
async def fetch_school_geometries_by_bbox(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    session: AsyncSession = Depends(get_session)
) -> FeatureCollection:
    """
    Retrieve schools within a bounding box.

    Args:
        xmin: Minimum x-coordinate (longitude)
        ymin: Minimum y-coordinate (latitude)
        xmax: Maximum x-coordinate (longitude)
        ymax: Maximum y-coordinate (latitude)
        session: Database session

    Returns:
        GeoJSON FeatureCollection of schools

    Raises:
        HTTPException: If no schools are found in the bounding box
    """
    rows = await get_school_geometries_by_bbox(
        session, xmin, ymin, xmax, ymax
    )

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No matches found for the given bounding box'
        )

    return create_geojson_from_rows(rows)


@route_school.get(
    '/radius',
    response_model=SchoolGeometryResponse,
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
                                'loc': ['query', 'school_id'],
                                'msg': 'value is not a valid integer',
                                'type': 'type_error.integer'
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=['Schulen'],
    description=(
        'Retrieves school geometries based on the provided latitude and longitude. '
        'The coordinates must be in the order: lat, lng.'
    )
)
async def fetch_school_geometries_by_lat_lng(
    lat: float,
    lng: float,
    session: AsyncSession = Depends(get_session)
) -> FeatureCollection:
    """
    Retrieve schools near a specific lat/lng point.

    Args:
        lat: Latitude
        lng: Longitude
        session: Database session

    Returns:
        GeoJSON FeatureCollection of schools

    Raises:
        HTTPException: If no schools are found near the coordinates
    """
    rows = await get_school_geometries_by_lat_lng(session, lat, lng)

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No matches found for coordinates ({lat}, {lng})'
        )

    return create_geojson_from_rows(rows)


@route_school.get(
    '/type',
    response_model=SchoolGeometryResponse,
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
                                'loc': ['query', 'school_id'],
                                'msg': 'value is not a valid integer',
                                'type': 'type_error.integer'
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=['Schulen'],
    description=(
        'Retrieves school geometries based on the provided school type. '
        'The school type must be provided as an integer.'
    )
)
async def fetch_school_geometries_by_school_type(
    school_type: int,
    session: AsyncSession = Depends(get_session)
) -> FeatureCollection:
    """
    Retrieve schools by school type.

    Args:
        school_type: ID of the school type
        session: Database session

    Returns:
        GeoJSON FeatureCollection of schools

    Raises:
        HTTPException: If no schools are found with the specified school type
    """
    rows = await get_school_geometries_by_school_type(session, school_type)

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No matches found for school type {school_type}'
        )

    return create_geojson_from_rows(rows)


@route_school.get(
    '/types',
    response_model=List[SchoolTypeResponse],
    responses={
        404: {
            'description': 'Not Found',
            'content': {
                'application/json': {
                    'example': {'detail': 'No matches found for school types'}
                }
            }
        }
    },
    tags=['Schulen'],
    description=(
        'Retrieves all available school types. '
        'The response includes the name and code of each school type.'
    )
)
async def fetch_school_types(
    session: AsyncSession = Depends(get_session)
) -> List[SchoolTypeResponse]:
    """
    Retrieve all available school types.

    Args:
        session: Database session

    Returns:
        List of school types with their codes and names

    Raises:
        HTTPException: If no school types are found
    """
    rows = await get_school_types(session)

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No matches found for school types'
        )

    return rows
