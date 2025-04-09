from sqlalchemy.sql import text, func, case
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
    Flurstueck
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
    ).label("parcel_number")

    area_hectares = (
        func.ST_Area(func.ST_Transform(Flurstueck.geometrie, 3587)) / 10000
    ).label("area_hectares")

    geojson = func.ST_AsGeoJSON(
        Flurstueck.geometrie, 15
    ).cast(JSONB).label("geojson")

    stmt = (
        select(
            DistrictNumber.district_name,
            DistrictNumber.district_number,
            Flurstueck.flur.label("field_number"),
            MunicipalityKey.municipality_name,
            Flurstueck.aktualit.label("last_update"),
            Flurstueck.lagebeztxt.label("place_description"),
            Flurstueck.gemarkung.label("cadastral_district_name"),
            Flurstueck.gemaschl.label("cadastral_district_number"),
            MunicipalityKey.municipality_key.label("municipality_number"),
            parcel_number_case,
            area_hectares,
            geojson,
        )
        .join(
            MunicipalityKey,
            MunicipalityKey.municipality_key == func.LPAD(
                cast(Flurstueck.gmdschl, String), 8, "0"
            ),
        )
        .join(
            DistrictNumber,
            DistrictNumber.district_number == func.LPAD(
                cast(Flurstueck.kreisschl, String), 5, "0"
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
    validated_key = sanitize_string(validated_key)

    stmt = text('''
    SELECT
        vg.ags AS municipality_key,
        mk.municipality_name AS municipality_name,
        vg.gen AS geographical_name,
        TO_CHAR(vg.beginn, 'DD.MM.YYYY') AS date_of_entry,
        ST_Area(ST_Transform(vg.geom, 3587)) AS shape_area,
        jsonb_build_object(
            'xmin', ST_XMin(agg.bbox),
            'ymin', ST_YMin(agg.bbox),
            'xmax', ST_XMax(agg.bbox),
            'ymax', ST_YMax(agg.bbox)
        ) AS bbox,
        ST_AsGeoJSON(vg.geom, 15)::jsonb AS geojson
    FROM
        de_municipality_keys AS mk
    LEFT JOIN vg25_gem AS vg
        ON mk.municipality_key = vg.ags
        AND vg.gf = 9
    LEFT JOIN (
        SELECT
            ags,
            ST_Extent(geom) AS bbox
        FROM
            vg25_gem
        GROUP BY ags
    ) AS agg
        ON vg.ags = agg.ags
    WHERE
        mk.municipality_key = :key
    ''')

    sql = stmt.bindparams(key=validated_key.lower())
    result = await session.execute(sql)

    return result.mappings().all()


async def get_municipality_by_name(
    session: AsyncSession,
    municipality_name: str
):
    validated_name = validate_not_none(municipality_name)
    validated_name = sanitize_string(validated_name)

    stmt = text('''
    SELECT
        vg.ags AS municipality_key,
        mk.municipality_name AS municipality_name,
        vg.gen AS geographical_name,
        TO_CHAR(vg.beginn, 'DD.MM.YYYY') AS date_of_entry,
        ST_Area(ST_Transform(vg.geom, 3587)) AS shape_area,
        jsonb_build_object(
            'xmin', ST_XMin(vg.geom),
            'ymin', ST_YMin(vg.geom),
            'xmax', ST_XMax(vg.geom),
            'ymax', ST_YMax(vg.geom)
        ) AS bbox,
        ST_AsGeoJSON(vg.geom, 15)::jsonb AS geojson
    FROM
        vg25_gem AS vg
    LEFT JOIN
        de_municipality_keys AS mk
        ON vg.ags = mk.municipality_key
    WHERE
        LOWER(vg.gen) LIKE :name
    ''')

    sql = stmt.bindparams(name=validated_name.lower())
    result = await session.execute(sql)

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
