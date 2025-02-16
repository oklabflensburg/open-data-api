from sqlalchemy.sql import func, text
from sqlalchemy.types import JSON
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..utils.parser import parse_date
from ..utils.validators import validate_positive_int32, validate_not_none
from ..schemas.archaeology import ArchaeologicalMonumentResponse
from ..models.archaeology import ArchaeologicalMonument, ArchaeologicalMonumentCategory, ArchaeologicalMonumentXCategory



async def get_archaeological_monument(session: AsyncSession, filters: dict):
    cte_stmt = (
        select(
            ArchaeologicalMonumentXCategory.monument_id,
            func.string_agg(ArchaeologicalMonumentCategory.label, ', ').label('category_labels')
        )
        .join(
            ArchaeologicalMonumentCategory,
            ArchaeologicalMonumentXCategory.category_id == ArchaeologicalMonumentCategory.id
        )
        .group_by(ArchaeologicalMonumentXCategory.monument_id)
        .cte('archaeological_monument_categories')
    )

    stmt = (
        select(
            ArchaeologicalMonument.id.label('monument_id'),
            cte_stmt.c.category_labels.label('object_category'),
            ArchaeologicalMonument.proper_name,
            ArchaeologicalMonument.object_number,
            ArchaeologicalMonument.district_name,
            ArchaeologicalMonument.municipality_name,
            ArchaeologicalMonument.object_description,
            ArchaeologicalMonument.object_significance,
            ArchaeologicalMonument.protection_scope,
            func.to_char(ArchaeologicalMonument.date_registered, 'DD.MM.YYYY').label('date_registered'),
            func.to_char(ArchaeologicalMonument.date_modified, 'DD.MM.YYYY').label('date_modified'),
            ArchaeologicalMonument.status,
            ArchaeologicalMonument.heritage_authority,
            ArchaeologicalMonument.municipality_key,
            cast(func.ST_AsGeoJSON(ArchaeologicalMonument.wkb_geometry, 15), JSON).label('geojson')
        )
        .join(cte_stmt, ArchaeologicalMonument.id == cte_stmt.c.monument_id, isouter=True)
    )

    # Apply multiple filters dynamically
    for column_name, filter_value in filters.items():
        column = getattr(ArchaeologicalMonument, column_name)

        # Handle date range queries
        if column_name in ['date_registered', 'date_modified']:
            parsed_date, date_operator = parse_date(filter_value)
            print(date_operator)

            if date_operator == '=':
                stmt = stmt.where(column == parsed_date)
            elif date_operator == '>':
                stmt = stmt.where(column > parsed_date)
            elif date_operator == '<':
                stmt = stmt.where(column < parsed_date)
            elif date_operator == '>=':
                stmt = stmt.where(column >= parsed_date)
            elif date_operator == '<=':
                stmt = stmt.where(column <= parsed_date)
            else:
                raise ValueError(f'Invalid operator: {date_operator}')
        else:
            stmt = stmt.where(column == filter_value)

    result = await session.execute(stmt)
    rows = result.mappings().all()

    if not rows:
        raise HTTPException(status_code=404, detail='No archaeological monument found with the given filters.')

    return rows
