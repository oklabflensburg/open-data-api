from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models


async def get_district(session: AsyncSession, district_id: int):
    result = await session.execute(select(models.District).where(id=district_id))
    
    return result.scalars().first()


async def get_districts(session: AsyncSession):
    result = await session.execute(select(models.District))

    return result.scalars().all()
