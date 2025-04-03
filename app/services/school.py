from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..utils.validators import validate_positive_int32, validate_utf8_string


async def get_school_by_slug(session: AsyncSession, slug: str):
    validated_slug = validate_utf8_string(slug)

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
        s.website,
        s.agency_number,
        st.name AS main_school_type,
        COALESCE(jsonb_agg(st2.name) FILTER (WHERE st2.name IS NOT NULL), '[]'::jsonb) AS school_types,
        s.slug
    FROM
        sh_school AS s
    LEFT JOIN
        sh_school_type AS st
        ON st.code = s.main_school_type
    LEFT JOIN
        sh_school_type AS st2
        ON (s.school_type & st2.code) != 0
    WHERE
        slug = :slug
    GROUP BY
        s.id, st.name
    ''')

    sql = stmt.bindparams(slug=validated_slug)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_school_by_id(session: AsyncSession, school_id: int):
    try:
        validated_school_id = validate_positive_int32(school_id)
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
        s.website,
        s.agency_number,
        st.name AS main_school_type,
        COALESCE(jsonb_agg(st2.name) FILTER (WHERE st2.name IS NOT NULL), '[]'::jsonb) AS school_types,
        s.slug
    FROM
        sh_school AS s
    LEFT JOIN
        sh_school_type AS st
        ON st.code = s.main_school_type
    LEFT JOIN
        sh_school_type AS st2
        ON (s.school_type & st2.code) != 0
    WHERE
        s.id = :school_id
    GROUP BY
        s.id, st.name
    ''')

    sql = stmt.bindparams(school_id=validated_school_id)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_school_geometries_by_bbox(
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
        sh_school
    WHERE
        ST_WITHIN(
            wkb_geometry,
            ST_MakeEnvelope(:xmin, :ymin, :xmax, :ymax, 4326)
        )
    ''')

    sql = stmt.bindparams(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_school_geometries_by_lat_lng(
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
        sh_school
    WHERE
        ST_DWithin(
            wkb_geometry::geography,
            ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography,
            :radius
        )
    ''')

    sql = stmt.bindparams(lat=lat, lng=lng, radius=radius)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]
