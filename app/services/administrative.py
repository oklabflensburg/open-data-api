from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession



async def get_parcel_meta_by_lat_lng(session: AsyncSession, lat: float, lng: float):
    stmt = text('''
    SELECT
        p.adv_id,
        p.start_time,
        p.field_number,
        p.parcel_number,
        p.municipality_number,
        p.cadastral_district_number,
        lp.cadastral_district_name,
        lp.municipality_name,
        ST_Area(ST_Transform(p.wkb_geometry, 3587)) AS shape_area,
        ST_AsGeoJSON(p.wkb_geometry, 15)::jsonb AS geojson
    FROM
        sh_alkis_parcel AS p
    JOIN
        de_cadastral_district_meta AS lp
        ON p.cadastral_district_number = lp.cadastral_district_number
    WHERE
        ST_Contains(
            wkb_geometry,
            ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)
        )
    ''')

    sql = stmt.bindparams(lat=lat, lng=lng)
    result = await session.execute(sql)

    return result.mappings().all()


async def get_municipality_by_key(session: AsyncSession, key: str):
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

    sql = stmt.bindparams(key=key.lower())
    result = await session.execute(sql)

    return result.mappings().all()


async def get_municipality_by_name(session: AsyncSession, name: str):
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

    query = f'{name.lower()}%'
    sql = stmt.bindparams(name=query)
    result = await session.execute(sql)

    return result.mappings().all()



async def get_municipality_by_query(session: AsyncSession, query: str):
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

    sql = stmt.bindparams(q=query.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]

