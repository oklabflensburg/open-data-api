from sqlalchemy import func
from sqlalchemy.sql import text, case
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils.validators import validate_not_none
from ..utils.sanitizer import sanitize_string

from ..models.administrative import (
    DistrictNumber,
    MunicipalityKey,
    Flurstueck,
    VG25Gem
)


async def get_parcel_meta_by_lat_lng(
    session: AsyncSession,
    lat: float,
    lng: float
):
    point = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)

    parcel_number_case = case(
        (
            Flurstueck.flstnrnen is not None,
            func.concat(
                cast(Flurstueck.flstnrzae, String),
                '/',
                cast(Flurstueck.flstnrnen, String),
            ),
        ),
        else_=cast(Flurstueck.flstnrzae, String),
    ).label('parcel_number')

    area_hectares = (
        func.ST_Area(func.ST_Transform(Flurstueck.geometrie, 3587)) / 10000
    ).label('area_hectares')

    geojson = func.ST_AsGeoJSON(
        Flurstueck.geometrie, 15
    ).cast(JSONB).label('geojson')

    stmt = (
        select(
            DistrictNumber.district_name,
            DistrictNumber.district_number,
            Flurstueck.flur.label('field_number'),
            MunicipalityKey.municipality_name,
            Flurstueck.aktualit.label('last_update'),
            Flurstueck.lagebeztxt.label('place_description'),
            Flurstueck.gemarkung.label('cadastral_district_name'),
            Flurstueck.gemaschl.label('cadastral_district_number'),
            MunicipalityKey.municipality_key.label('municipality_number'),
            parcel_number_case,
            area_hectares,
            geojson,
        )
        .join(
            MunicipalityKey,
            MunicipalityKey.municipality_key == func.LPAD(
                cast(Flurstueck.gmdschl, String), 8, '0'
            ),
        )
        .join(
            DistrictNumber,
            DistrictNumber.district_number == func.LPAD(
                cast(Flurstueck.kreisschl, String), 5, '0'
            ),
        )
        .where(func.ST_Contains(Flurstueck.geometrie, point))
    )

    result = await session.execute(stmt)
    return result.mappings().all()


async def get_municipality_by_key(
    session: AsyncSession,
    municipality_key: str
):
    validated_key = validate_not_none(municipality_key)
    validated_key = sanitize_string(validated_key.lower())

    bbox_cte = (
        select(
            VG25Gem.ags.label('ags'),
            func.ST_Extent(VG25Gem.geom).label('bbox')
        )
        .group_by(VG25Gem.ags)
        .cte('agg')
    )

    stmt = (
        select(
            VG25Gem.ags.label('municipality_key'),
            MunicipalityKey.municipality_name.label('municipality_name'),
            VG25Gem.gen.label('geographical_name'),
            func.to_char(VG25Gem.beginn, 'DD.MM.YYYY').label('date_of_entry'),
            func.ST_Area(func.ST_Transform(
                VG25Gem.geom, 3587)).label('shape_area'),
            func.jsonb_build_object(
                'xmin', func.ST_XMin(bbox_cte.c.bbox),
                'ymin', func.ST_YMin(bbox_cte.c.bbox),
                'xmax', func.ST_XMax(bbox_cte.c.bbox),
                'ymax', func.ST_YMax(bbox_cte.c.bbox),
            ).label('bbox'),
            cast(func.ST_AsGeoJSON(VG25Gem.geom, 15), JSONB).label('geojson'),
        )
        .select_from(MunicipalityKey)
        .outerjoin(
            VG25Gem,
            (
                MunicipalityKey.municipality_key == VG25Gem.ags
            ) & (
                VG25Gem.gf == 9
            )
        )
        .outerjoin(
            bbox_cte,
            VG25Gem.ags == bbox_cte.c.ags
        )
        .where(MunicipalityKey.municipality_key == validated_key)
    )

    result = await session.execute(stmt)

    return result.mappings().all()


async def get_municipality_by_name(
    session: AsyncSession,
    municipality_name: str
):
    validated_name = validate_not_none(municipality_name)
    validated_name = sanitize_string(validated_name.lower())

    stmt = (
        select(
            VG25Gem.ags.label('municipality_key'),
            MunicipalityKey.municipality_name.label('municipality_name'),
            VG25Gem.gen.label('geographical_name'),
            func.to_char(VG25Gem.beginn, 'DD.MM.YYYY').label('date_of_entry'),
            func.ST_Area(func.ST_Transform(
                VG25Gem.geom, 3587)).label('shape_area'),
            func.jsonb_build_object(
                'xmin', func.ST_XMin(VG25Gem.geom),
                'ymin', func.ST_YMin(VG25Gem.geom),
                'xmax', func.ST_XMax(VG25Gem.geom),
                'ymax', func.ST_YMax(VG25Gem.geom),
            ).label('bbox'),
            cast(func.ST_AsGeoJSON(VG25Gem.geom, 15), JSONB).label('geojson'),
        )
        .select_from(VG25Gem)
        .outerjoin(
            MunicipalityKey,
            VG25Gem.ags == MunicipalityKey.municipality_key
        )
        .where(func.lower(VG25Gem.gen).like(validated_name))
    )

    result = await session.execute(stmt)
    return result.mappings().all()


async def get_municipality_by_query(
    session: AsyncSession,
    query: str
):
    validated_query = validate_not_none(query)
    sanitized_query = sanitize_string(validated_query)

    stmt = text('''
    SELECT
        gem.ags AS municipality_key,
        gem.gen AS geographical_name,
        CASE
            WHEN gem.ibz != 60 THEN krs.bez || ' ' || krs.gen
            ELSE lan.gen
        END AS region_name,
        jsonb_build_object(
            'xmin', ST_XMin(gem.geom),
            'ymin', ST_YMin(gem.geom),
            'xmax', ST_XMax(gem.geom),
            'ymax', ST_YMax(gem.geom)
        ) AS bbox
    FROM
        vg25_gem AS gem
    JOIN
        vg250_krs AS krs
    ON
        gem.sn_l = krs.sn_l AND gem.sn_r = krs.sn_r AND gem.sn_k = krs.sn_k
    JOIN
        vg250_lan AS lan
    ON
        krs.sn_l = lan.sn_l
    WHERE
        (LOWER(gem.gen) % :q OR LOWER(gem.gen) ILIKE '%' || :q || '%')
        AND gem.gf = 4
        AND krs.gf = 4
        AND lan.gf = 4
    ORDER BY
        (LOWER(gem.gen) ILIKE :q || '%') DESC,
        (LOWER(gem.gen) ILIKE '%' || :q || '%') DESC,
        similarity(LOWER(gem.gen), :q) DESC
    LIMIT 10
    ''')

    sql = stmt.bindparams(q=sanitized_query.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]
