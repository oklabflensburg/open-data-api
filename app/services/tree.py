from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.tree import StreetTreeRegister

async def get_tree_by_id(session: AsyncSession, tree_id: int):
    model = StreetTreeRegister

    stmt = select(model).where(model.id == tree_id)
    result = await session.execute(stmt)
    row = result.scalars().first()

    return row
