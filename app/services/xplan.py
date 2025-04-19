from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession


async def get_plan_by_lat_lng(
    session: AsyncSession,
    lat: float,
    lng: float
):
    stmt = text('''
    SELECT
        b.name AS plan_name,
        b.nummer AS plan_number,
        b.gemeinde AS municipality,
        CASE
            WHEN ST_Area(ST_Transform(b.geometry, 3587)) < 10000 THEN
                ST_Area(ST_Transform(b.geometry, 3587)) || ' m²'
            ELSE ST_Area(ST_Transform(b.geometry, 3587)) / 10000 || ' ha'
        END AS shape_area,
        ST_AsGeoJSON(b.geometry, 15)::jsonb AS geojson
    FROM
        xplan.bp_plan AS b
    WHERE
        ST_Contains(b.geometry, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326))
    ''')

    sql = stmt.bindparams(lat=lat, lng=lng)
    result = await session.execute(sql)

    return result.mappings().all()
