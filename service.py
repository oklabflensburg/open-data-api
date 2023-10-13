from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

import models



async def get_monuments(session: AsyncSession):
    model = models.Monument
    result = await session.execute(select(model))

    return result.scalars().all()



async def get_accident_details_by_city(session: AsyncSession, query: str):
    sql = text('''
    SELECT jsonb_build_object(
        'type', 'FeatureCollection',
        'center', COUNT(fc),
        'features', jsonb_agg(fc.feature)
    )
    FROM (
        SELECT jsonb_build_object(
            'type', 'Feature',
            -- 'id', objectid::text,
            'geometry', ST_AsGeoJSON(ST_Transform(a.wkb_geometry, 4326))::jsonb,
            'properties', to_jsonb(ul) || to_jsonb(uw) || to_jsonb(um) ||
            jsonb_build_object('ags', concat(a.uland, a.uregbez, a.ukreis, a.ugemeinde),
            'ujahr', a.ujahr, 'ustunde', a.ustunde) ||
            COALESCE(to_jsonb(t), to_jsonb(tt)) ||
            COALESCE(to_jsonb(k), to_jsonb(kk)) ||
            COALESCE(to_jsonb(i), to_jsonb(ii)) ||
            COALESCE(to_jsonb(p), to_jsonb(pp)) ||
            COALESCE(to_jsonb(r), to_jsonb(rr)) ||
            COALESCE(to_jsonb(j), to_jsonb(jj)) ||
            COALESCE(to_jsonb(f), to_jsonb(ff)) ||
            COALESCE(to_jsonb(s), to_jsonb(ss)) ||
            COALESCE(to_jsonb(m), to_jsonb(mm)) ||
            COALESCE(to_jsonb(g), to_jsonb(gg))
        ) AS feature
        FROM accidents AS a

        JOIN vg250 AS v
        ON ST_WITHIN(a.wkb_geometry, v.wkb_geometry)

        LEFT JOIN uwochentag AS uw
        ON a.uwochentag = uw.id::text

        LEFT JOIN uland AS ul
        ON a.uland = LPAD(ul.id::text, 2, '0')

        LEFT JOIN umonat AS um
        ON a.umonat = LPAD(um.id::text, 2, '0')

        LEFT JOIN uart AS t
        ON a.uart = t.id::text
        LEFT JOIN (SELECT '' AS uart) AS tt
        ON a.uart IS NULL

        LEFT JOIN ukategorie AS k
        ON a.ukategorie = k.id::text
        LEFT JOIN (SELECT '' AS ukategorie) AS kk
        ON a.ukategorie IS NULL

        LEFT JOIN istrad AS r
        ON a.istrad = r.id::text
        LEFT JOIN (SELECT '' AS istrad) AS rr
        ON a.istrad IS NULL

        LEFT JOIN ulichtverh AS i
        ON a.ulichtverh = i.id::text
        LEFT JOIN (SELECT '' AS ulichtverh) AS ii
        ON a.ulichtverh IS NULL

        LEFT JOIN istpkw AS j
        ON a.istpkw = j.id::text
        LEFT JOIN (SELECT '' AS istpkw) AS jj
        ON a.istpkw IS NULL

        LEFT JOIN istfuss AS f
        ON a.istfuss = f.id::text
        LEFT JOIN (SELECT '' AS istfuss) AS ff
        ON a.istfuss IS NULL

        LEFT JOIN istsonstig AS s
        ON a.istsonstig = s.id::text
        LEFT JOIN (SELECT '' AS istsonstig) AS ss
        ON a.istsonstig IS NULL

        LEFT JOIN istgkfz AS g
        ON a.istgkfz = g.id::text
        LEFT JOIN (SELECT '' AS istgkfz) AS gg
        ON a.istgkfz IS NULL

        LEFT JOIN istkrad AS m
        ON a.istkrad = m.id::text
        LEFT JOIN (SELECT '' AS istkrad) AS mm
        ON a.istkrad IS NULL

        LEFT JOIN utyp1 AS p
        ON a.utyp1 = p.id::text
        LEFT JOIN (SELECT '' AS utyp1) AS pp
        ON a.utyp1 IS NULL

        WHERE LOWER(v.gen) = :q
    ) AS fc;
    ''')

    stmt = sql.bindparams(q=query)
    result = await session.execute(stmt)

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
