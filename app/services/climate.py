from sqlalchemy.sql import func, text, bindparam
from sqlalchemy.types import JSON
from sqlalchemy.sql.expression import cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased
from geoalchemy2 import Geography

from ..utils.validators import validate_not_none
from ..utils.sanitizer import sanitize_string

from ..models.climate import (
    DwdStationReference,
    WeatherStation,
    MosmixStation
)

from ..models.administrative import Vg250Gem


async def get_all_mosmix_stations(session: AsyncSession):
    model = MosmixStation

    geojson = cast(func.ST_AsGeoJSON(
        model.wkb_geometry, 15), JSON).label('geojson')

    query = select(
        model.station_id,
        model.icao_code,
        model.station_name,
        model.station_elevation,
        geojson
    )

    result = await session.execute(query)

    return result.mappings().all()


async def get_dwd_stations_by_municipality_key(
    session: AsyncSession,
    municipality_key: str
):
    validated_key = validate_not_none(municipality_key)
    validated_key = sanitize_string(validated_key)

    geojson = cast(func.ST_AsGeoJSON(
        DwdStationReference.wkb_geometry, 15), JSON).label('geojson')
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
            func.to_char(DwdStationReference.recording_start,
                         'DD.MM.YYYY').label('recording_start'),
            func.to_char(DwdStationReference.recording_end,
                         'DD.MM.YYYY').label('recording_end'),
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

    geojson = cast(func.ST_AsGeoJSON(
        model.wkb_geometry, 15), JSON).label('geojson')

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


async def get_mosmix_geometries_by_bbox(
    session: AsyncSession,
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float
):
    model = MosmixStation

    geojson = cast(func.ST_AsGeoJSON(
        model.wkb_geometry, 15), JSON).label('geojson')

    envelope = func.ST_MakeEnvelope(
        bindparam('xmin'),
        bindparam('ymin'),
        bindparam('xmax'),
        bindparam('ymax'),
        4326
    )

    stmt = (
        select(
            model.station_id,
            model.station_name,
            model.station_elevation,
            geojson
        )
        .where(
            func.ST_WITHIN(model.wkb_geometry, envelope),
            func.ST_IsValid(model.wkb_geometry)
        )
    )

    result = await session.execute(
        stmt,
        {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
    )

    rows = result.mappings().all()

    return rows


async def get_mosmix_geometries_by_radius(
    session: AsyncSession,
    lat: float,
    lng: float,
    radius: float
):
    model = MosmixStation

    geojson = cast(func.ST_AsGeoJSON(
        model.wkb_geometry, 15), JSON).label('geojson')

    point = func.ST_SetSRID(func.ST_MakePoint(
        bindparam('lng'),
        bindparam('lat')
    ), 4326)

    stmt = (
        select(
            model.station_id,
            model.station_name,
            geojson
        )
        .where(
            func.ST_DWithin(
                cast(model.wkb_geometry, Geography),
                cast(point, Geography),
                bindparam('radius')
            ),
            func.ST_IsValid(model.wkb_geometry)
        )
    )

    result = await session.execute(
        stmt,
        {'lat': lat, 'lng': lng, 'radius': radius}
    )

    rows = result.mappings().all()

    return rows


async def get_mosmix_nearest_geometriey_by_position(
    session: AsyncSession,
    lat: float,
    lng: float
):
    model = MosmixStation

    geojson = cast(func.ST_AsGeoJSON(
        model.wkb_geometry, 15), JSON).label('geojson')

    point = func.ST_SetSRID(func.ST_MakePoint(
        bindparam('lng'),
        bindparam('lat')
    ), 4326)

    stmt = (
        select(
            model.station_id,
            model.station_name,
            geojson
        )
        .where(
            func.ST_IsValid(model.wkb_geometry)
        )
        .order_by(
            func.ST_Distance(
                cast(model.wkb_geometry, Geography),
                cast(point, Geography)
            )
        )
        .limit(1)
    )

    result = await session.execute(
        stmt,
        {'lat': lat, 'lng': lng}
    )

    rows = result.mappings().first()

    return rows
