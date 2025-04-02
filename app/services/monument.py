from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..utils.validators import validate_positive_int32, validate_utf8_string


async def get_monument_by_slug(session: AsyncSession, slug: str):
    validated_slug = validate_utf8_string(slug)

    stmt = text('''
    SELECT
        ST_AsGeoJSON(b.polygon_center, 15)::jsonb AS geojson,
        COALESCE(
            NULLIF(b.street, '') || ' ' || NULLIF(b.housenumber, ''),
            NULLIF(b.street, '')
        ) AS label,
        b.id,
        b.postcode,
        b.city,
        b.slug,
        b.layer_name,
        b.district,
        b.municipality,
        b.street,
        b.housenumber,
        CASE
            WHEN m.description IS NOT NULL
            AND LEFT(m.description, 12) != 'Alteintragung'
            THEN m.description
            ELSE b.description
        END AS description,
        b.monument_type,
        b.monument_function,
        b.object_number,
        COALESCE(m.image_url, b.photo_link) AS photo_link,
        b.detail_link,
        b.last_update
    FROM
        sh_monument_boundary_processed AS b
    LEFT JOIN sh_monument AS m
        ON b.object_number = m.object_number
    WHERE
        b.slug = :slug
    ''')

    sql = stmt.bindparams(slug=validated_slug)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_monument_by_object_number(
    session: AsyncSession,
    object_number: str
):
    stmt = text('''
    SELECT
        ST_AsGeoJSON(b.polygon_center, 15)::jsonb AS geojson,
        COALESCE(
            NULLIF(b.street, '') || ' ' || NULLIF(b.housenumber, ''),
            NULLIF(b.street, '')
        ) AS label,
        b.postcode,
        b.city,
        b.slug,
        b.layer_name,
        b.district,
        b.municipality,
        b.street,
        b.housenumber,
       CASE
            WHEN m.description IS NOT NULL
            AND LEFT(m.description, 12) != 'Alteintragung'
            THEN m.description
            ELSE b.description
        END AS description,
        b.monument_type,
        b.monument_function,
        b.object_number,
        COALESCE(m.image_url, b.photo_link) AS photo_link,
        b.detail_link,
        b.last_update
    FROM
        sh_monument_boundary_processed AS b
    LEFT JOIN sh_monument AS m
        ON b.object_number = m.object_number
    WHERE
        b.object_number = :object_number
    ''')

    sql = stmt.bindparams(object_number=object_number)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_monument_by_id(session: AsyncSession, monument_id: int):
    try:
        validated_monument_id = validate_positive_int32(monument_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    stmt = text('''
    SELECT
        ST_AsGeoJSON(b.polygon_center, 15)::jsonb AS geojson,
        COALESCE(
            NULLIF(b.street, '') || ' ' || NULLIF(b.housenumber, ''),
            NULLIF(b.street, '')
        ) AS label,
        b.id,
        b.postcode,
        b.city,
        b.slug,
        b.layer_name,
        b.district,
        b.municipality,
        b.street,
        b.housenumber,
       CASE
            WHEN m.description IS NOT NULL
            AND LEFT(m.description, 12) != 'Alteintragung'
            THEN m.description
            ELSE b.description
        END AS description,
        b.monument_type,
        b.monument_function,
        b.object_number,
        COALESCE(m.image_url, b.photo_link) AS photo_link,
        b.detail_link,
        b.last_update
    FROM
        sh_monument_boundary_processed AS b
    LEFT JOIN sh_monument AS m
        ON b.object_number = m.object_number
    WHERE
        b.id = :monument_id
    ''')

    sql = stmt.bindparams(monument_id=validated_monument_id)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_monument_geometries_by_bbox(
    session: AsyncSession,
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float
):
    stmt = text('''
    SELECT
        id,
        ST_AsGeoJSON(polygon_center) AS geom,
        COALESCE(
            NULLIF(street, '') || ' ' || NULLIF(housenumber, ''),
            NULLIF(street, '')
        ) AS label
    FROM
        sh_monument_boundary_processed
    WHERE
        ST_WITHIN(
            polygon_center,
            ST_MakeEnvelope(:xmin, :ymin, :xmax, :ymax, 4326)
        )
        AND ST_IsValid(polygon_center)
        AND ST_IsSimple(polygon_center)
    ''')

    sql = stmt.bindparams(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_monument_geometries_by_lat_lng(
    session: AsyncSession,
    lat: float,
    lng: float,
    radius: float = 1000
):
    stmt = text('''
    SELECT
        id,
        ST_AsGeoJSON(polygon_center) AS geom,
        COALESCE(
            NULLIF(street, '') || ' ' || NULLIF(housenumber, ''),
            NULLIF(street, '')
        ) AS label
    FROM
        sh_monument_boundary_processed
    WHERE
        ST_DWithin(
            polygon_center::geography,
            ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography,
            :radius
        )
        AND ST_IsValid(polygon_center)
        AND ST_IsSimple(polygon_center)
    ''')

    sql = stmt.bindparams(lat=lat, lng=lng, radius=radius)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]
