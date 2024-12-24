from sqlalchemy.sql import func, text
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..models.biotope import ShBiotopeOrigin
from ..utils.sanitizer import sanitize_string


async def get_biotope_origin_meta(session: AsyncSession, code: str):
    try:
        value = sanitize_string(code.lower())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = ShBiotopeOrigin

    stmt = select(model.description).where(func.lower(model.code) == value)

    result = await session.execute(stmt)

    return result.scalars().all()



async def get_biotope_meta_by_lat_lng(session: AsyncSession, lat: float, lng: float):
    stmt = text('''
    SELECT
        bm.code,
        bm.designation,
        b.kartierdatum AS mapping_date,
        b.biotopbez AS description,
        b.wertbiotop AS valuable_biotope,
        b.herkunft AS mapping_origin,
        bo.description AS mapping_origin_description,
        bo.remark AS mapping_origin_remark,
        b.ortnr AS place_number,
        CASE
            WHEN b.btschutz_1 IS NOT NULL AND b.btschutz_2 IS NOT NULL THEN b.btschutz_1 || ', ' || b.btschutz_2
            WHEN b.btschutz_1 IS NOT NULL THEN b.btschutz_1
            WHEN b.btschutz_2 IS NOT NULL THEN b.btschutz_2
            ELSE NULL
        END AS protection_reason,
        b.lrt_typ_1 AS habitat_type_1,
        b.lrt_typ_2 AS habitat_type_2,
        ht1.label AS habitat_label_1,
        ht2.label AS habitat_label_2,
        b.gemeindename AS place_name,
        ST_Area(ST_Transform(b.wkb_geometry, 3587)) AS shape_area,
        ST_AsGeoJSON(b.wkb_geometry, 15)::jsonb AS geojson
    FROM
        sh_biotope AS b
    JOIN
        sh_biotope_key AS bm
        ON b.hauptcode = bm.code
    LEFT JOIN sh_biotope_origin AS bo
        ON b.herkunft = bo.code
    LEFT JOIN de_habitat_types AS ht1
        ON b.lrt_typ_1 = ht1.code
    LEFT JOIN de_habitat_types AS ht2
        ON b.lrt_typ_2 = ht2.code
    WHERE
        ST_Contains(b.wkb_geometry, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326))
    ''')

    sql = stmt.bindparams(lat=lat, lng=lng)
    result = await session.execute(sql)

    return result.mappings().all()
