from sqlalchemy.sql import func, text, bindparam
from sqlalchemy.types import JSON 
from sqlalchemy.sql.expression import cast 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased
from fastapi import HTTPException

from ..utils.validators import validate_not_none
from ..utils.sanitizer import sanitize_string
from ..models.climate import DwdStationReference, WeatherStation
from ..models.administrative import Vg250Gem



async def get_dwd_stations_by_municipality_key(session: AsyncSession, municipality_key: str):
    validated_key = validate_not_none(municipality_key)
    validated_key = sanitize_string(validated_key)

    geojson = cast(func.ST_AsGeoJSON(DwdStationReference.wkb_geometry, 15), JSON).label('geojson')
    gem_alias = aliased(Vg250Gem)

    stmt = (
        select(
            DwdStationReference.station_name,
            DwdStationReference.station_id,
            DwdStationReference.identifier,
            DwdStationReference.station_code,
            DwdStationReference.station_elevation,
            DwdStationReference.river_basin_id,
            DwdStationReference.state_name,
            func.to_char(DwdStationReference.recording_start, 'DD.MM.YYYY').label('recording_start'),
            func.to_char(DwdStationReference.recording_end, 'DD.MM.YYYY').label('recording_end'),
            geojson,
        )
        .join(
            gem_alias,
            func.ST_Contains(
                func.ST_Transform(gem_alias.geom, 4326),
                DwdStationReference.wkb_geometry
            )
        )
        .where(
            gem_alias.ags == bindparam('municipality_key'),
            gem_alias.gf == 4,
            DwdStationReference.recording_end > func.current_date() - text("INTERVAL '1 week'")
        )
    )

    result = await session.execute(stmt, {'municipality_key': validated_key})
    return result.mappings().all()


async def get_weather_service_stations(session: AsyncSession):
    model = WeatherStation

    geojson = cast(func.ST_AsGeoJSON(model.wkb_geometry, 15), JSON).label('geojson')

    query = select(
        model.station_id,
        func.to_char(model.start_date, 'DD.MM.YYYY').label('start_date'),
        func.to_char(model.end_date, 'DD.MM.YYYY').label('end_date'),
        model.station_elevation,
        model.station_name,
        model.state_name,
        model.submission,
        geojson
    )

    result = await session.execute(query)

    return result.mappings().all()



async def get_energy_source_meta(session: AsyncSession):
    model = EnergySourceMeta

    result = await session.execute(select(model))
    return result.scalars().all()


async def get_energy_state_meta(session: AsyncSession):
    stmt = text('''
    SELECT
        esm.id, esm.name, lan.sn_l AS state_id,
        CASE WHEN lan.geom IS NOT NULL THEN
            jsonb_build_object(
            'xmin', ST_XMin(lan.geom),
            'ymin', ST_YMin(lan.geom),
            'xmax', ST_XMax(lan.geom),
            'ymax', ST_YMax(lan.geom))
        ELSE NULL END AS bbox
    FROM de_energy_state_meta AS esm
    LEFT JOIN
        vg250_lan AS lan
    ON
        lan.gen = esm.name
    AND
        lan.gf = 4
    ORDER BY
        lan.sn_l
    ''')

    result = await session.execute(stmt)
    rows = result.mappings().all()

    return [dict(row) for row in rows]
