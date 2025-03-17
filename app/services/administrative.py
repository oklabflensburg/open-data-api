from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..utils.validators import validate_not_none
from ..utils.sanitizer import sanitize_string



async def get_parcel_meta_by_lat_lng(session: AsyncSession, lat: float, lng: float):
    stmt = text('''
    SELECT
        kreis AS district_name,
        kreisschl AS district_number,
        flur AS field_number,
        gemeinde AS municipality_name,
        gmdschl AS municipality_number,
        gemarkung AS cadastral_district_name,
        gemaschl AS cadastral_district_number, 
        LPAD(gmdschl::text, 8, '0') AS municipality_number,
        CASE                                                                      
            WHEN flstnrnen IS NOT NULL THEN flstnrzae::text || '/' || flstnrnen::text                                                                           
            ELSE flstnrzae::text                                                                           
        END AS parcel_number,                                                                                                                                 
        ST_Area(ST_Transform(ST_GeomFromEWKB(geometrie), 3587)) / 10000 AS area_hectares,
        ST_AsGeoJSON(geometrie, 15)::jsonb AS geojson                                                                    
    FROM flurstueck
    WHERE
        ST_Contains(
            geometrie,
            ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)
        )
    ''')

    sql = stmt.bindparams(lat=lat, lng=lng)
    result = await session.execute(sql)

    return result.mappings().all()


async def get_municipality_by_key(session: AsyncSession, municipality_key: str):
    try:
        validated_key = validate_not_none(municipality_key, 'query', 'municipality_key')
        validated_key = sanitize_string(validated_key)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    stmt = text('''
    SELECT
        mk.municipality_key AS municipality_key,
        mk.municipality_name AS municipality_name,
        vg.gen AS geographical_name,
        vg.ewz AS population,
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
    LEFT JOIN vg250_gem AS vg
        ON mk.municipality_key = vg.ags
        AND vg.gf = 4
    LEFT JOIN (
        SELECT
            ags,
            ST_Extent(geom) AS bbox
        FROM
            vg250_gem
        GROUP BY ags
    ) AS agg
        ON vg.ags = agg.ags
    WHERE
        LOWER(mk.municipality_key) = :key
    ''')

    sql = stmt.bindparams(key=validated_key.lower())
    result = await session.execute(sql)

    return result.mappings().all()


async def get_municipality_by_name(session: AsyncSession, municipality_name: str):
    try:
        validated_name = validate_not_none(municipality_name, 'query', 'municipality_name')
        validated_name = sanitize_string(validated_name)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    stmt = text('''
    SELECT
        mk.municipality_key AS municipality_key,
        mk.municipality_name AS municipality_name,
        vg.gen AS geographical_name,
        vg.ewz AS population,
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
        vg250_gem AS vg
    JOIN
        de_municipality_keys AS mk
        ON vg.ags = mk.municipality_key
        AND vg.gf = 4
    WHERE
        LOWER(vg.gen) LIKE :name
    ''')

    sql = stmt.bindparams(name=validated_name.lower())
    result = await session.execute(sql)

    return result.mappings().all()



async def get_municipality_by_query(session: AsyncSession, query: str):
    try:
        validated_query = validate_not_none(query, 'query', 'query')
        sanitized_query = sanitize_string(validated_query)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

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
        vg250_gem AS gem
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
