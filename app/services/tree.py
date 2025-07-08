from sqlalchemy import select, case, literal_column, func
from sqlalchemy.sql import exists, and_, not_, text
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tree import StreetTreeRegister

async def get_tree_by_id(session: AsyncSession, tree_id: int):
    model = StreetTreeRegister

    stmt = select(model).where(model.id == tree_id)
    result = await session.execute(stmt)
    row = result.scalars().first()

    return row

async def get_tree_by_species(session: AsyncSession):
    # Alias for subquery
    gef = aliased(StreetTreeRegister)

    stmt = (
        select(
            StreetTreeRegister.id,
            StreetTreeRegister.tree_number,
            StreetTreeRegister.street,
            StreetTreeRegister.species,
            StreetTreeRegister.type,
            func.round(
                func.ST_X(func.ST_Transform(StreetTreeRegister.geom, 4326)).cast('numeric'),
                6
            ).label("lon"),
            func.round(
                func.ST_Y(func.ST_Transform(StreetTreeRegister.geom, 4326)).cast('numeric'),
                6
            ).label("lat"),
            case(
                (
                    StreetTreeRegister.species.ilike("%Tilia%"), 1,
                ),
                (
                    StreetTreeRegister.species.ilike("%Acer%"), 2,
                ),
                (
                    StreetTreeRegister.species.ilike("%Quercus%"), 3,
                ),
                (
                    StreetTreeRegister.species.ilike("%Fagus%"), 4,
                ),
                (
                    StreetTreeRegister.species.ilike("%Betula%"), 5,
                ),
                (
                    StreetTreeRegister.species.ilike("%Carpinus%"), 6,
                ),
                else_=0,
            ).label("species_index")
        )
        .where(
            StreetTreeRegister.type == 'bestand',
            not_(
                exists()
                .where(
                    and_(
                        gef.type == 'gefaellt',
                        gef.tree_number == StreetTreeRegister.tree_number,
                        gef.street == StreetTreeRegister.street,
                    )
                )
            )
        )
        .order_by(StreetTreeRegister.species)
    )

    result = await session.execute(stmt)
    rows = result.mappings().all()

    return [dict(row) for row in rows]
