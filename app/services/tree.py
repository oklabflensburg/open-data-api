from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.tree import StreetTreeRegister

async def get_tree_by_id(session: AsyncSession, tree_id: int):
    model = StreetTreeRegister

    stmt = select(model).where(model.id == tree_id)
    result = await session.execute(stmt)
    row = result.scalars().first()

    return row

async def get_tree_by_species(session: AsyncSession):
    stmt = text('''
        SELECT
            tr.id,
            tr.tree_number,
            tr.street,
            tr.species,
            tr.type,
            ROUND(ST_X(ST_Transform(tr.geom, 4326))::numeric, 6) AS lon,
            ROUND(ST_Y(ST_Transform(tr.geom, 4326))::numeric, 6) AS lat,
            CASE
                WHEN tr.species ILIKE '%Tilia%' THEN 1
                WHEN tr.species ILIKE '%Acer%' THEN 2
                WHEN tr.species ILIKE '%Quercus%' THEN 3
                WHEN tr.species ILIKE '%Fagus%' THEN 4
                WHEN tr.species ILIKE '%Betula%' THEN 5
                WHEN tr.species ILIKE '%Carpinus%' THEN 6
                ELSE 0
            END AS species_index
        FROM flensburg.street_tree_register tr
        WHERE tr.type = 'bestand'
          AND NOT EXISTS (
            SELECT 1
            FROM flensburg.street_tree_register gef
            WHERE gef.type = 'gefaellt'
              AND gef.tree_number = tr.tree_number
              AND gef.street = tr.street
          )
        ORDER BY tr.species
    ''')

    result = await session.execute(stmt)
    rows = result.mappings().all()

    return [dict(row) for row in rows]