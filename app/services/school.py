from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..utils.validators import validate_positive_int32, validate_utf8_string


async def get_school_by_slug(session: AsyncSession, slug: str):
    validated_slug = validate_utf8_string(slug)

    stmt = text('''
    SELECT
        ST_AsGeoJSON(
            COALESCE(
                s.wkb_geometry,
                CASE
                    WHEN s.longitude IS NOT NULL AND s.latitude IS NOT NULL THEN
                        ST_SetSRID(
                            ST_MakePoint(
                                s.longitude::double precision,
                                s.latitude::double precision
                            ),
                            4326
                        )
                END
            ),
            15
        )::jsonb AS geojson,
        s.id,
        s.source_id,
        s.name,
        s.city,
        s.zipcode,
        s.street,
        s.house_number,
        s.telephone,
        s.fax,
        s.email,
        s.website,
        s.longitude,
        s.latitude,
        s.agency_number,
        st.name AS main_school_type,
        COALESCE(jsonb_agg(st2.name) FILTER (WHERE st2.name IS NOT NULL), '[]'::jsonb) AS school_types,
        s.wikidata_p13491,
        s.wikidata_id,
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

    return rows


async def get_school_by_id(session: AsyncSession, school_id: int):
    try:
        validated_school_id = validate_positive_int32(school_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    stmt = text('''
    SELECT
        ST_AsGeoJSON(
            COALESCE(
                s.wkb_geometry,
                CASE
                    WHEN s.longitude IS NOT NULL AND s.latitude IS NOT NULL THEN
                        ST_SetSRID(
                            ST_MakePoint(
                                s.longitude::double precision,
                                s.latitude::double precision
                            ),
                            4326
                        )
                END
            ),
            15
        )::jsonb AS geojson,
        s.id,
        s.source_id,
        s.name,
        s.city,
        s.zipcode,
        s.street,
        s.house_number,
        s.telephone,
        s.fax,
        s.email,
        s.website,
        s.longitude,
        s.latitude,
        s.agency_number,
        st.name AS main_school_type,
        COALESCE(jsonb_agg(st2.name) FILTER (WHERE st2.name IS NOT NULL), '[]'::jsonb) AS school_types,
        s.wikidata_p13491,
        s.wikidata_id,
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

    return rows


async def get_school_geometries_by_bbox(
    session: AsyncSession,
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float
):
    stmt = text('''
    WITH school_geometry AS (
        SELECT
            id,
            school_type,
            name,
            COALESCE(
                wkb_geometry,
                CASE
                    WHEN longitude IS NOT NULL AND latitude IS NOT NULL THEN
                        ST_SetSRID(
                            ST_MakePoint(
                                longitude::double precision,
                                latitude::double precision
                            ),
                            4326
                        )
                END
            ) AS geom
        FROM
            sh_school
    )
    SELECT
        id,
        school_type,
        ST_AsGeoJSON(geom, 15) AS geojson,
        name AS label
    FROM
        school_geometry
    WHERE
        geom IS NOT NULL
    AND
        ST_WITHIN(
            geom,
            ST_MakeEnvelope(:xmin, :ymin, :xmax, :ymax, 4326)
        )
    AND
        ST_IsValid(geom)
    ''')

    sql = stmt.bindparams(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return rows


async def get_school_geometries_by_lat_lng(
    session: AsyncSession,
    lat: float,
    lng: float,
    radius: int
):
    stmt = text('''
    WITH school_geometry AS (
        SELECT
            id,
            school_type,
            name,
            COALESCE(
                wkb_geometry,
                CASE
                    WHEN longitude IS NOT NULL AND latitude IS NOT NULL THEN
                        ST_SetSRID(
                            ST_MakePoint(
                                longitude::double precision,
                                latitude::double precision
                            ),
                            4326
                        )
                END
            ) AS geom
        FROM
            sh_school
    )
    SELECT
        id,
        school_type,
        ST_AsGeoJSON(geom, 15) AS geojson,
        name AS label
    FROM
        school_geometry
    WHERE
        geom IS NOT NULL
    AND
        ST_DWithin(
            geom::geography,
            ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography,
            :radius
        )
    AND
        ST_IsValid(geom)
    ''')

    sql = stmt.bindparams(lat=lat, lng=lng, radius=radius)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return rows


async def get_school_geometries_by_school_type(
    session: AsyncSession,
    school_type: int
):
    stmt = text('''
    WITH school_geometry AS (
        SELECT
            id,
            school_type,
            name,
            COALESCE(
                wkb_geometry,
                CASE
                    WHEN longitude IS NOT NULL AND latitude IS NOT NULL THEN
                        ST_SetSRID(
                            ST_MakePoint(
                                longitude::double precision,
                                latitude::double precision
                            ),
                            4326
                        )
                END
            ) AS geom
        FROM
            sh_school
    )
    SELECT
        id,
        school_type,
        ST_AsGeoJSON(geom, 15) AS geojson,
        name AS label
    FROM
        school_geometry
    WHERE
        (school_type & :school_type) != 0
    AND
        geom IS NOT NULL
    AND
        ST_IsValid(geom)
    ''')

    sql = stmt.bindparams(school_type=school_type)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return rows


async def get_school_types(
    session: AsyncSession
):
    stmt = text('''
    SELECT
        code,
        name
    FROM
        sh_school_type
    ''')

    result = await session.execute(stmt)
    rows = result.mappings().all()

    return rows
