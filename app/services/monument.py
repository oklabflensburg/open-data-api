from sqlalchemy.sql import func, text
from sqlalchemy.types import JSON
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..utils.validators import validate_positive_int32, validate_not_none
from ..schemas.monument import ArchaeologicalMonumentResponse
from ..models.monument import ArchaeologicalMonument, ArchaeologicalMonumentCategory, ArchaeologicalMonumentXCategory



async def get_monument_by_slug(session: AsyncSession, slug: str):
    stmt = text('''
    WITH monument_reasons AS (
        SELECT
            mxr.monument_id,
            string_agg(mr.label, ', ') AS reason_labels
        FROM
            sh_monument_x_reason AS mxr
        JOIN
            sh_monument_reason AS mr
        ON
            mxr.reason_id = mr.id
        GROUP BY
            mxr.monument_id
    ),
    monument_scopes AS (
        SELECT
            mxs.monument_id,
            string_agg(ms.label, ', ') AS scope_labels
        FROM
            sh_monument_x_scope AS mxs
        JOIN
            sh_monument_scope AS ms
        ON
            mxs.scope_id = ms.id
        GROUP BY
            mxs.monument_id
    )
    SELECT
        ST_AsGeoJSON(m.wkb_geometry, 15)::jsonb AS geojson,
        COALESCE(m.street || ' ' || m.housenumber, m.street) AS label,
        m.id,
        m.object_id,
        m.slug,
        m.street,
        m.housenumber,
        m.postcode,
        m.city,
        m.image_url,
        m.designation,
        m.description,
        m.monument_type,
        r.reason_labels AS monument_reason,
        s.scope_labels AS monument_scope
    FROM
        sh_monument AS m
    LEFT JOIN
        monument_reasons AS r
    ON
        m.id = r.monument_id
    LEFT JOIN
        monument_scopes AS s
    ON
        m.id = s.monument_id
    WHERE
        m.slug = :slug
    ''')

    sql = stmt.bindparams(slug=slug)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]



async def get_monument_geometries_by_bbox(session: AsyncSession, xmin: float, ymin: float, xmax: float, ymax: float):
    stmt = text('''
    SELECT id, street, housenumber, ST_AsGeoJSON(wkb_geometry) AS geom

    FROM sh_monument

    WHERE ST_Within(wkb_geometry, ST_MakeEnvelope(:xmin, :ymin, :xmax, :ymax, 4326))
    ''')

    sql = stmt.bindparams(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]



async def get_monument_by_id(session: AsyncSession, monument_id: int):
    try:
        validated_monument_id = validate_positive_int32(monument_id, 'query', 'monument_id')
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    stmt = text('''
    WITH monument_reasons AS (
        SELECT
            mxr.monument_id,
            string_agg(mr.label, ', ') AS reason_labels
        FROM
            sh_monument_x_reason AS mxr
        JOIN
            sh_monument_reason AS mr
        ON
            mxr.reason_id = mr.id
        GROUP BY
            mxr.monument_id
    ),
    monument_scopes AS (
        SELECT
            mxs.monument_id,
            string_agg(ms.label, ', ') AS scope_labels
        FROM
            sh_monument_x_scope AS mxs
        JOIN
            sh_monument_scope AS ms
        ON
            mxs.scope_id = ms.id
        GROUP BY
            mxs.monument_id
    )
    SELECT
        ST_AsGeoJSON(m.wkb_geometry, 15)::jsonb AS geojson,
        COALESCE(m.street || ' ' || m.housenumber, m.street) AS label,
        m.id,
        m.object_id,
        m.slug,
        m.street,
        m.housenumber,
        m.postcode,
        m.city,
        m.image_url,
        m.designation,
        m.description,
        m.monument_type,
        r.reason_labels AS monument_reason,
        s.scope_labels AS monument_scope
    FROM
        sh_monument AS m
    LEFT JOIN
        monument_reasons AS r
    ON
        m.id = r.monument_id
    LEFT JOIN
        monument_scopes AS s
    ON
        m.id = s.monument_id
    WHERE
        m.id = :monument_id
    ''')

    sql = stmt.bindparams(monument_id=validated_monument_id)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]



async def get_archaeological_monument_by_id(session: AsyncSession, monument_id: int):
    # Define the CTE for categories
    cte_stmt = (
        select(
            ArchaeologicalMonumentXCategory.monument_id,
            func.string_agg(ArchaeologicalMonumentCategory.label, ', ').label("category_labels")
        )
        .join(
            ArchaeologicalMonumentCategory,
            ArchaeologicalMonumentXCategory.category_id == ArchaeologicalMonumentCategory.id
        )
        .group_by(ArchaeologicalMonumentXCategory.monument_id)
        .cte('archaeological_monument_categories')
    )

    stmt = (
        select(
            ArchaeologicalMonument.id.label('monument_id'),
            cte_stmt.c.category_labels.label('object_category'),
            ArchaeologicalMonument.proper_name,
            ArchaeologicalMonument.object_number,
            ArchaeologicalMonument.district_name,
            ArchaeologicalMonument.municipality_name,
            ArchaeologicalMonument.object_description,
            ArchaeologicalMonument.object_significance,
            ArchaeologicalMonument.protection_scope,
            func.to_char(ArchaeologicalMonument.date_registered, 'DD.MM.YYYY').label('date_registered'),
            func.to_char(ArchaeologicalMonument.date_modified, 'DD.MM.YYYY').label('date_modified'),
            ArchaeologicalMonument.status,
            ArchaeologicalMonument.heritage_authority,
            ArchaeologicalMonument.municipality_key,
            cast(func.ST_AsGeoJSON(ArchaeologicalMonument.wkb_geometry, 15), JSON).label('geojson')
        )
        .join(cte_stmt, ArchaeologicalMonument.id == cte_stmt.c.monument_id, isouter=True)
        .where(ArchaeologicalMonument.id == monument_id)
    )

    result = await session.execute(stmt)
    return result.mappings().all()
