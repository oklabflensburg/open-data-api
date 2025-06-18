from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.tree import StreetTreeRegister

async def get_tree_by_id(session: AsyncSession, tree_id: int):
    model = StreetTreeRegister

    stmt = select(model.id).where(model.id == tree_id)
    result = await session.execute(stmt)
    row = result.mappings().one_or_none()

    return row
