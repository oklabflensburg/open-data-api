from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..utils.validators import validate_positive_int32



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
        m.object_id,
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
