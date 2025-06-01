from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..utils.validators import validate_positive_int32, validate_utf8_string


async def get_police_station_by_id(session: AsyncSession, station_id: int):
    try:
        validated_station_id = validate_positive_int32(station_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    stmt = text('''
    SELECT
        ST_AsGeoJSON(s.wkb_geometry, 15)::jsonb AS geojson,
        s.id,
        s.name,
        s.city,
        s.zipcode,
        s.street,
        s.house_number,
        s.telephone,
        s.fax,
        s.email,
        s.website
    FROM
        sh_police_station AS s
    WHERE
        s.id = :station_id
    ''')

    sql = stmt.bindparams(station_id=validated_station_id)
    result = await session.execute(sql)
    row = result.mappings().one_or_none()

    return row


async def get_police_station_geometries_by_bbox(
    session: AsyncSession,
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float
):
    stmt = text('''
    SELECT
        id,
        ST_AsGeoJSON(wkb_geometry, 15) AS geojson,
        name AS label
    FROM
        sh_police_station
    WHERE
        ST_WITHIN(
            wkb_geometry,
            ST_MakeEnvelope(:xmin, :ymin, :xmax, :ymax, 4326)
        )
    AND
        ST_IsValid(wkb_geometry)
    ''')

    sql = stmt.bindparams(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return rows


async def get_police_station_geometries_by_lat_lng(
    session: AsyncSession,
    lat: float,
    lng: float,
    radius: float = 1000
):
    stmt = text('''
    SELECT
        id,
        ST_AsGeoJSON(wkb_geometry, 15) AS geojson,
        name AS label
    FROM
        sh_police_station
    WHERE
        ST_DWithin(
            wkb_geometry::geography,
            ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography,
            :radius
        )
    AND
        ST_IsValid(wkb_geometry)
    ''')

    sql = stmt.bindparams(lat=lat, lng=lng, radius=radius)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return rows
