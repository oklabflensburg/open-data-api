from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession


async def get_plan_by_lat_lng(
    session: AsyncSession,
    lat: float,
    lng: float
):
    stmt = text('''
    SELECT
        ST_AsGeoJSON(b.geometry, 15)::jsonb AS geojson
    FROM
        xplan.bp_plan AS b
    WHERE
        ST_Contains(b.geometry, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326))
    ''')

    sql = stmt.bindparams(lat=lat, lng=lng)
    result = await session.execute(sql)

    return result.mappings().all()
