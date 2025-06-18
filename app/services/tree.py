from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from ..models.tree import Street_tree_register

async def get_tree_by_id(session: AsyncSession, tree_id: int):
    model = Street_tree_register

    stmt = select(model.id).where(model.id = tree_id)

    result = await session.execute()
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
