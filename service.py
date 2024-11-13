from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

import models



async def get_municipality_by_key(session: AsyncSession, key: str):
    stmt = text('''
    SELECT
        jsonb_build_object(
            'municipality_key', mk.municipality_key,
            'municipality_name', mk.municipality_name,
            'geographical_name', vg.gen,
            'population', vg.ewz,
            'date_of_entry', TO_CHAR(vg.beginn, 'DD.MM.YYYY'),
            'shape_area', ST_Area(ST_Transform(vg.geom, 3587)),
            'bbox', jsonb_build_object(
                'xmin', ST_XMin(agg.bbox),
                'ymin', ST_YMin(agg.bbox),
                'xmax', ST_XMax(agg.bbox),
                'ymax', ST_YMax(agg.bbox)
            ),
            'geojson', ST_AsGeoJSON(vg.geom)::jsonb
        ) as municipality
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
        jsonb_build_object(
            'municipality_key', mk.municipality_key,
            'municipality_name', mk.municipality_name,
            'geographical_name', vg.gen,
            'population', vg.ewz,
            'date_of_entry', TO_CHAR(vg.beginn, 'DD.MM.YYYY'),
            'shape_area', ST_Area(ST_Transform(vg.geom, 3587)),
            'bbox', jsonb_build_object(
                'xmin', ST_XMin(vg.geom),
                'ymin', ST_YMin(vg.geom),
                'xmax', ST_XMax(vg.geom),
                'ymax', ST_YMax(vg.geom)
            ),
            'geojson', ST_AsGeoJSON(vg.geom)::jsonb
        ) as municipality
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



async def get_biotop_origin(session: AsyncSession, code: str):
    stmt = text('''
    SELECT
        bo.description
    FROM
        sh_biotop_origin AS bo
    WHERE
        LOWER(bo.code) = :code
    ''')

    sql = stmt.bindparams(code=code.lower())
    result = await session.execute(sql)

    return result.mappings().all()



async def get_biotop_meta(session: AsyncSession, lat: float, lng: float):
    stmt = text('''
    SELECT
        bm.code,
        bm.designation,
        b.biotopbez AS description,
        b.wertbiotop AS valuable_biotope,
        b.herkunft AS mapping_origin,
        b.ortnr AS place_number,
        b.gemeindename AS place_name,
        ST_Area(ST_Transform(b.shape, 3587)) AS shape_area,
        ST_AsGeoJSON(b.shape) AS geojson
    FROM
        sh4_bksh_belangflaechen AS b
    JOIN
        sh_biotop_meta AS bm
        ON b.hauptcode = bm.code
    WHERE
        ST_Contains(b.shape, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326))
    ''')

    sql = stmt.bindparams(lat=lat, lng=lng)
    result = await session.execute(sql)

    return result.mappings().all()


async def get_parcel_meta(session: AsyncSession, lat: float, lng: float):
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
        ST_Area(ST_Transform(wkb_geometry, 3587)) AS shape_area,
        ST_AsGeoJSON(wkb_geometry) AS geojson
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



async def get_monuments(session: AsyncSession, object_id: int):
    stmt = text('''
    SELECT
        json_build_object(
            'type', 'FeatureCollection',
            'crs', json_build_object(
                'type', 'name',
                'properties', json_build_object(
                    'name', 'urn:ogc:def:crs:OGC:1.3:CRS84'
                )
            ),
            'features', json_agg(
                json_build_object(
                    'type', 'Feature',
                    'geometry', ST_AsGeoJSON(m.wkb_geometry)::json,
                    'properties', json_build_object(
                        'object_id', m.object_id,
                        'place_name', m.place_name,
                        'address', m.address,
                        'postal_code', m.postal_code,
                        'image_url', m.image_url,
                        'designation', m.designation,
                        'description', m.description,
                        'monument_type', m.monument_type,
                        'reasons', (
                            SELECT string_agg(mr.label, ', ')
                            FROM monument_reason AS mr
                            WHERE mxr.monument_id = m.id
                        )
                    )
                )
            )
        )
    FROM monuments AS m

    JOIN monument_x_reason AS mxr
    ON mxr.monument_id = m.id

    JOIN monument_reason AS mr
    ON mxr.reason_id = mr.id

    JOIN vg250gem AS v
    ON ST_Within(ST_GeomFromEWKB(m.wkb_geometry), ST_GeomFromEWKB(v.wkb_geometry))

    WHERE m.object_id = :q
    ''')

    sql = stmt.bindparams(q=object_id)
    result = await session.execute(sql)

    return result.scalars().all()



async def get_demographics_meta(session: AsyncSession):
    stmt = text('''
    SELECT json_build_object(
        cmd.table_name, json_agg(
            json_build_object(cmd.column_name, cmd.column_label)
        )
    ) AS column_meta_data

    FROM column_meta_data cmd

    JOIN i18n AS i
    ON cmd.i18n_id = i.id

    GROUP BY cmd.table_name
    ORDER BY cmd.table_name
    ''')

    result = await session.execute(stmt)

    return result.scalars().all()



async def get_accident_meta(session: AsyncSession):
    stmt = text('''
    SELECT json_build_object(
        'istfuss', (
            SELECT json_agg(row_to_json(f))
            FROM istfuss AS f
        ),
        'istgkfz', (
            SELECT json_agg(row_to_json(g))
            FROM istgkfz AS g
        ),
        'istkrad', (
            SELECT json_agg(row_to_json(k))
            FROM istkrad AS k
        ),
        'istpkw', (
            SELECT json_agg(row_to_json(p))
            FROM istpkw AS p
        ),
        'istrad', (
            SELECT json_agg(row_to_json(r))
            FROM istrad AS r
        ),
        'istsonstig', (
            SELECT json_agg(row_to_json(s))
            FROM istsonstig AS s
        ),
        'uart', (
            SELECT json_agg(row_to_json(a))
            FROM uart AS a
        ),
        'ukategorie', (
            SELECT json_agg(row_to_json(c))
            FROM ukategorie AS c
        ),
        'uland', (
            SELECT json_agg(row_to_json(l))
            FROM uland AS l
        ),
        'ulichtverh', (
            SELECT json_agg(row_to_json(y))
            FROM ulichtverh AS y
        ),
        'ustrzustan', (
            SELECT json_agg(row_to_json(z))
            FROM ustrzustan AS z
        ),
        'uwochentag', (
            SELECT json_agg(row_to_json(w))
            FROM uwochentag AS w
        ),
        'umonat', (
            SELECT json_agg(row_to_json(m))
            FROM umonat AS m
        ),
        'utyp1', (
            SELECT json_agg(row_to_json(t))
            FROM utyp1 AS t
        )
    ) AS meta
    ''')

    result = await session.execute(stmt)

    return result.scalars().all()


async def get_accident_details_by_city(session: AsyncSession, query: str):
    stmt = text('''
    SELECT json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(fc.feature)
    ) AS data
    FROM (
        SELECT json_build_object(
        'type', 'Feature',
        'geometry', ST_AsGeoJSON(ST_Transform(a.wkb_geometry, 4326))::json,
        'properties', json_build_object(
            'ags', a.ags, 'ujahr', a.ujahr,
            'ustunde', a.ustunde, 'uwochentag', a.uwochentag,
            'umonat', a.umonat, 'uland', a.uland, 'uart', a.uart, 'utyp1', a.utyp1,
            'ukategorie', a.ukategorie, 'ulichtverh', a.ulichtverh,
            'istrad', a.istrad, 'istpkw', a.istpkw, 'istfuss', a.istfuss,
            'istgkfz', a.istgkfz, 'istkrad', a.istkrad, 'istsonstig', a.istsonstig)
        ) AS feature
        FROM accidents AS a

        JOIN vg250gem AS v
        ON a.ags = v.ags

        WHERE LOWER(v.gen) = :q
    ) AS fc
    ''')

    sql = stmt.bindparams(q=query.lower())
    result = await session.execute(sql)

    return result.scalars().all()



async def get_district_details(session: AsyncSession):
    sql = text('''
    WITH districts_summary AS (
        SELECT
            rd.year,
            json_build_object(
                'sum_residents', SUM(rd.residents),
                'sum_districts_area', ROUND(SUM(CAST(ST_Area(d.wkb_geometry::geography) / 1000000 AS numeric)), 2)
            ) AS summary
        FROM
            districts AS d
        LEFT JOIN
            residents_by_districts AS rd
        ON d.id = rd.district_id
        WHERE
            rd.year = 2021
        GROUP BY
            rd.year
    ),
    district_summary AS (
        SELECT
            rd.year,
            json_object_agg(
                'detail', json_build_object(
                    'district_id', d.id,
                    'district_name', d.name,
                    'residents', rd.residents,
                    'births', bd.births,
                    'birth_rate', bd.birth_rate,
                    'age_ratio', ard.quotient,
                    'age_groups', json_build_object(
                        'age_18_to_under_30', agrd.age_18_to_under_30,
                        'age_30_to_under_45', agrd.age_30_to_under_45,
                        'age_45_to_under_65', agrd.age_45_to_under_65,
                        'age_65_to_under_80', agrd.age_65_to_under_80,
                        'age_0_to_under_7', agrd.age_0_to_under_7,
                        'age_60_and_above', agrd.age_60_and_above,
                        'age_80_and_above', agrd.age_80_and_above,
                        'age_to_under_18', cad.residents,
                        'age_18_to_under_65', ra1865d.residents,
                        'age_65_and_above', ra65ad.residents
                    ),
                    'employed_residents', epid.residents,
                    'employment_rate', epid.employment_rate,
                    'unemployed_residents', ued.residents,
                    'unemployment_characteristics', json_build_object(
                        'percentage_sgb_iii', uecd.percentage_sgb_iii,
                        'percentage_sgb_ii', uecd.percentage_sgb_ii,
                        'percentage_foreign_citizenship', uecd.percentage_foreign_citizenship,
                        'percentage_female', uecd.percentage_female,
                        'percentage_age_under_25', uecd.percentage_age_under_25
                    ),
                    'housing_benefit', hbd.residents,
                    'housing_assistance', json_build_object(
                        'notices_of_rent_arrears', hacd.notices_of_rent_arrears,
                        'termination_rent_arrears', hacd.termination_rent_arrears,
                        'termination_for_conduct', hacd.termination_for_conduct,
                        'action_for_eviction', hacd.action_for_eviction,
                        'general_consulting', hacd.general_consulting,
                        'eviction_notice', hacd.eviction_notice,
                        'eviction_carried', hacd.eviction_carried
                    ),
                    'risk_of_homelessness', hrhd.residents,
                    'benefits_age_15_to_under_65', json_build_object(
                        'employable_with_benefits', ba1565d.employable_with_benefits,
                        'unemployment_benefits', ba1565d.unemployment_benefits,
                        'basic_income', ba1565d.basic_income,
                        'assisting_benefits', ba1565d.assisting_benefits
                    ),
                    'benefits_characteristics', json_build_object(
                        'beneficiaries_sgbii', bfd.residents,
                        'unemployability', bcd.unemployability,
                        'employability', bcd.employability,
                        'percentage_females', bcd.percentage_females,
                        'percentage_single_parents', bcd.percentage_single_parents,
                        'percentage_foreign_citizenship', bcd.percentage_foreign_citizenship
                    ),
                    'inactive_beneficiaries_in_households', iad.residents,
                    'basic_benefits_income', json_build_object(
                        'male', bbid.male,
                        'female', bbid.female,
                        'age_18_to_under_65', bbid.age_18_to_under_65,
                        'age_65_and_above', bbid.age_65_and_above
                    ),
                    'migration_background', json_build_object(
                        'foreign_citizenship', mbd.foreign_citizenship,
                        'german_citizenship', mbd.german_citizenship
                    )
                )
            ) AS district
        FROM
            districts AS d
        LEFT JOIN
            residents_by_districts AS rd
        ON d.id = rd.district_id
        LEFT JOIN
            births_by_districts AS bd
        ON d.id = bd.district_id
        AND bd.year = rd.year
        LEFT JOIN
            age_ratio_by_districts AS ard
        ON d.id = ard.district_id
        AND ard.year = rd.year
        LEFT JOIN
            children_age_under_18_by_districts AS cad
        ON d.id = cad.district_id
        AND cad.year = rd.year
        LEFT JOIN
            age_groups_of_residents_by_districts AS agrd
        ON d.id = agrd.district_id
        AND agrd.year = rd.year
        LEFT JOIN
            residents_age_18_to_under_65_by_districts AS ra1865d
        ON d.id = ra1865d.district_id
        AND rd.year = ra1865d.year
        LEFT JOIN
            residents_age_65_and_above_by_districts AS ra65ad
        ON d.id = ra65ad.district_id
        AND ra65ad.year = rd.year
        LEFT JOIN
            migration_background_by_districts AS mbd
        ON d.id = mbd.district_id
        AND mbd.year = rd.year
        LEFT JOIN
            employed_with_pension_insurance_by_districts AS epid
        ON d.id = epid.district_id
        AND rd.year = epid.year
        LEFT JOIN
            unemployed_residents_by_districts AS ued
        ON d.id = ued.district_id
        AND rd.year = ued.year
        LEFT JOIN
            unemployed_residents_by_districts_categorized AS uecd
        ON d.id = uecd.district_id
        AND rd.year = uecd.year
        LEFT JOIN
            housing_benefit_by_districts AS hbd
        ON d.id = hbd.district_id
        AND rd.year = hbd.year
        LEFT JOIN
            housing_assistance_cases_by_districts AS hacd
        ON d.id = hacd.district_id
        AND rd.year = hacd.year
        LEFT JOIN
            households_at_risk_of_homelessness_by_districts AS hrhd
        ON d.id = hrhd.district_id
        AND rd.year = hrhd.year
        LEFT JOIN
            beneficiaries_age_15_to_under_65_by_districts AS ba1565d
        ON d.id = ba1565d.district_id
        AND rd.year = ba1565d.year
        LEFT JOIN
            beneficiaries_by_districts AS bfd
        ON d.id = bfd.district_id
        AND rd.year = bfd.year
        LEFT JOIN
            beneficiaries_characteristics_by_districts AS bcd
        ON d.id = bcd.district_id
        AND rd.year = bcd.year
        LEFT JOIN
            inactive_beneficiaries_in_households_by_districts AS iad
        ON d.id = iad.district_id
        AND rd.year = iad.year
        LEFT JOIN
            basic_benefits_income_by_districts AS bbid
        ON d.id = bbid.district_id
        AND rd.year = bbid.year
        WHERE
            rd.year = 2021
        GROUP BY
            d.id, rd.year
        ORDER BY
            d.id, rd.year
    ),
    summary AS (
        SELECT year, summary
        FROM districts_summary
    )
    SELECT jsonb_build_object(
        'summary', (SELECT summary FROM summary WHERE year = ds.year),
        'detail', json_agg(ds.district->'detail')
    ) AS final_json
    FROM district_summary AS ds
    GROUP BY ds.year
    ''')

    result = await session.execute(sql)

    return result.scalars().all()



async def get_districts(session: AsyncSession):
    model = models.District
    result = await session.execute(select(model.id, model.name))

    return result.all()


async def get_district(session: AsyncSession, district_id: int):
    model = models.District
    result = await session.execute(select(model.id, model.name).filter(model.id==district_id))

    return result.first()



async def get_household_types(session: AsyncSession):
    model = models.HouseholdType
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_household_type(session: AsyncSession, household_type_id: int):
    model = models.HouseholdType
    result = await session.execute(select(model).filter(model.id==household_type_id))

    return result.scalars().all()



async def get_residents_by_age_groups(session: AsyncSession):
    model = models.AgeGroupsOfResident
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_by_age_group(session: AsyncSession, age_group_id: int):
    model = models.AgeGroupsOfResident
    result = await session.execute(select(model).filter(model.id==age_group_id))

    return result.scalars().all()



async def get_residents_non_germans(session: AsyncSession):
    model = models.NonGermanNationalsResidenceStatus
    result = await session.execute(select(model))

    return result.scalars().all()



async def get_residents_debt_counseling(session: AsyncSession):
    model = models.DebtCounselingOfResidents
    result = await session.execute(select(model))

    return result.scalars().all()



async def get_residents_education_support(session: AsyncSession):
    model = models.ChildEducationSupport
    result = await session.execute(select(model))

    return result.scalars().all()



async def get_residents_by_districts(session: AsyncSession):
    model = models.ResidentsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_by_district(session: AsyncSession, district_id: int):
    model = models.ResidentsByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_births_by_districts(session: AsyncSession):
    model = models.BirthsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_births_by_district(session: AsyncSession, district_id: int):
    model = models.BirthsByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_employed_by_districts(session: AsyncSession):
    model = models.EmployedWithPensionInsuranceByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_employed_by_district(session: AsyncSession, district_id: int):
    model = models.EmployedWithPensionInsuranceByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_ageratio_by_districts(session: AsyncSession):
    model = models.AgeRatioByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_ageratio_by_district(session: AsyncSession, district_id: int):
    model = models.AgeRatioByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_basicbenefits_by_districts(session: AsyncSession):
    model = models.BasicBenefitsIncomeByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_basicbenefits_by_district(session: AsyncSession, district_id: int):
    model = models.BasicBenefitsIncomeByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_ageunder18_by_districts(session: AsyncSession):
    model = models.ChildrenAgeUnder18ByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_ageunder18_by_district(session: AsyncSession, district_id: int):
    model = models.ChildrenAgeUnder18ByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_age18tounder65_by_districts(session: AsyncSession):
    model = models.ResidentsAge18ToUnder65ByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_age18tounder65_by_district(session: AsyncSession, district_id: int):
    model = models.ResidentsAge18ToUnder65ByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_age65andabove_by_districts(session: AsyncSession):
    model = models.ResidentsAge65AndAboveByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_age65andabove_by_district(session: AsyncSession, district_id: int):
    model = models.ResidentsAge65AndAboveByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_agegroups_by_districts(session: AsyncSession):
    model = models.AgeGroupsOfResidentsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_agegroups_by_district(session: AsyncSession, district_id: int):
    model = models.AgeGroupsOfResidentsByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_beneficiaries_by_districts(session: AsyncSession):
    model = models.BeneficiariesByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()



async def get_residents_unemployed_by_districts(session: AsyncSession):
    model = models.UnemployedResidentsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_unemployed_by_district(session: AsyncSession, district_id: int):
    model = models.UnemployedResidentsByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_unemployed_by_categories_by_districts(session: AsyncSession):
    model = models.UnemployedCategorizedResidentsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_unemployed_by_categories_by_district(session: AsyncSession, district_id: int):
    model = models.UnemployedCategorizedResidentsByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_beneficiaries_inactive_by_districts(session: AsyncSession):
    model = models.InactiveBeneficiariesInHouseholdsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_beneficiaries_by_district(session: AsyncSession, district_id: int):
    model = models.BeneficiariesByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_beneficiaries_characteristics_by_districts(session: AsyncSession):
    model = models.BeneficiariesCharacteristicsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_beneficiaries_inactive_by_district(session: AsyncSession, district_id: int):
    model = models.InactiveBeneficiariesInHouseholdsByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_beneficiaries_age15tounder65_by_districts(session: AsyncSession):
    model = models.BeneficiariesAge15ToUnder65ByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_beneficiaries_age15tounder65_by_district(session: AsyncSession, district_id: int):
    model = models.BeneficiariesAge15ToUnder65ByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_beneficiaries_characteristics_by_district(session: AsyncSession, district_id: int):
    model = models.BeneficiariesCharacteristicsByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_migration_background_by_districts(session: AsyncSession):
    model = models.MigrationBackgroundByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_migration_background_by_district(session: AsyncSession, district_id: int):
    model = models.MigrationBackgroundByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_housing_assistance_by_districts(session: AsyncSession):
    model = models.HousingAssistanceCasesByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_housing_assistance_by_district(session: AsyncSession, district_id: int):
    model = models.HousingAssistanceCasesByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_housing_benefit_by_districts(session: AsyncSession):
    model = models.HousingBenefitByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_housing_benefit_by_district(session: AsyncSession, district_id: int):
    model = models.HousingBenefitByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_risk_homelessness_by_districts(session: AsyncSession):
    model = models.HouseholdsAtRiskOfHomelessnessByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_risk_homelessness_by_district(session: AsyncSession, district_id: int):
    model = models.HouseholdsAtRiskOfHomelessnessByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()
