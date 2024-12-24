from sqlalchemy.sql import func, text, bindparam
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from ..models.accident import DeAccidentMeta
from ..utils.sanitizer import sanitize_string



async def get_accident_meta(session: AsyncSession):
    model = DeAccidentMeta
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_accident_details_by_city(session: AsyncSession, query: str):
    try:
        value = sanitize_string(query.lower())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    stmt = text('''
    SELECT json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(fc.feature)
    ) AS data
    FROM (
        SELECT json_build_object(
        'type', 'Feature',
        'geometry', ST_AsGeoJSON(ap.geom)::json,
        'properties', json_build_object(
            'ujahr', ap.ujahr, 'ustunde', ap.ustunde, 'uwochentag', ap.uwochentag,
            'umonat', ap.umonat, 'uland', ap.uland, 'uart', ap.uart, 'utyp1', ap.utyp1,
            'ukategorie', ap.ukategorie, 'ulichtverh', ap.ulichtverh, 'istrad', ap.istrad,
            'istpkw', ap.istpkw, 'istfuss', ap.istfuss, 'istgkfz', ap.istgkfz,
            'istkrad', ap.istkrad, 'istsonstig', ap.istsonstig)
        ) AS feature
        FROM vg250_gem AS vg

        JOIN de_accident_points AS ap
        ON ST_Within(ap.geom, vg.geom)

        WHERE LOWER(vg.gen) = :q
        AND vg.gf = 4
    ) AS fc
    ''')

    sql = stmt.bindparams(q=value)
    result = await session.execute(sql)

    return result.scalars().all()
