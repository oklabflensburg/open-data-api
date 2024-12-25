from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from ..utils.validators import validate_positive_int32, validate_not_none
from ..models.demographic import *



async def get_demographics_meta(session: AsyncSession):
    stmt = text('''
    SELECT json_build_object(
        cmd.table_name, json_agg(
            json_build_object(cmd.column_name, cmd.column_label)
        )
    ) AS column_meta_data

    FROM fl_column_meta_data cmd

    JOIN fl_i18n AS i
    ON cmd.i18n_id = i.id

    GROUP BY cmd.table_name
    ORDER BY cmd.table_name
    ''')

    result = await session.execute(stmt)

    return result.scalars().all()



async def get_district_details(session: AsyncSession):
    sql = text('''
    WITH districts_summary AS (
        SELECT
            rd.year,
            json_build_object(
                'sum_residents', SUM(rd.residents),
                'sum_districts_area', ROUND(SUM(CAST( ST_Area(ST_Transform(d.geom, 3587)) / 1000000 AS numeric)), 2)
            ) AS summary
        FROM
            fl_district AS d
        LEFT JOIN
            fl_residents_by_district AS rd
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
            fl_district AS d
        LEFT JOIN
            fl_residents_by_district AS rd
        ON d.id = rd.district_id
        LEFT JOIN
            fl_births_by_district AS bd
        ON d.id = bd.district_id
        AND bd.year = rd.year
        LEFT JOIN
            fl_age_ratio_by_district AS ard
        ON d.id = ard.district_id
        AND ard.year = rd.year
        LEFT JOIN
            fl_children_age_under_18_by_district AS cad
        ON d.id = cad.district_id
        AND cad.year = rd.year
        LEFT JOIN
            fl_age_groups_by_district AS agrd
        ON d.id = agrd.district_id
        AND agrd.year = rd.year
        LEFT JOIN
            fl_residents_age_18_to_under_65_by_district AS ra1865d
        ON d.id = ra1865d.district_id
        AND rd.year = ra1865d.year
        LEFT JOIN
            fl_residents_age_65_and_above_by_district AS ra65ad
        ON d.id = ra65ad.district_id
        AND ra65ad.year = rd.year
        LEFT JOIN
            fl_migration_background_by_district AS mbd
        ON d.id = mbd.district_id
        AND mbd.year = rd.year
        LEFT JOIN
            fl_employed_with_pension_insurance_by_district AS epid
        ON d.id = epid.district_id
        AND rd.year = epid.year
        LEFT JOIN
            fl_unemployed_residents_by_district AS ued
        ON d.id = ued.district_id
        AND rd.year = ued.year
        LEFT JOIN
            fl_unemployed_residents_categorized_by_district AS uecd
        ON d.id = uecd.district_id
        AND rd.year = uecd.year
        LEFT JOIN
            fl_housing_benefit_by_district AS hbd
        ON d.id = hbd.district_id
        AND rd.year = hbd.year
        LEFT JOIN
            fl_housing_assistance_cases_by_district AS hacd
        ON d.id = hacd.district_id
        AND rd.year = hacd.year
        LEFT JOIN
            fl_risk_homelessness_by_district AS hrhd
        ON d.id = hrhd.district_id
        AND rd.year = hrhd.year
        LEFT JOIN
            fl_beneficiaries_age_15_to_under_65_by_district AS ba1565d
        ON d.id = ba1565d.district_id
        AND rd.year = ba1565d.year
        LEFT JOIN
            fl_beneficiaries_by_district AS bfd
        ON d.id = bfd.district_id
        AND rd.year = bfd.year
        LEFT JOIN
            fl_beneficiaries_characteristics_by_district AS bcd
        ON d.id = bcd.district_id
        AND rd.year = bcd.year
        LEFT JOIN
            fl_inactive_beneficiaries_households_by_district AS iad
        ON d.id = iad.district_id
        AND rd.year = iad.year
        LEFT JOIN
            fl_basic_benefits_income_by_district AS bbid
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
    model = District
    result = await session.execute(select(model.id.label('district_id'), model.name.label('district_name')))

    return result.mappings().all()


async def get_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = District
    result = await session.execute(select(model.id, model.name).filter(model.id==validated_district_id))

    return result.first()



async def get_household_types(session: AsyncSession):
    model = HouseholdType
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_household_type(session: AsyncSession, household_type_id: int):
    model = HouseholdType
    result = await session.execute(select(model).filter(model.id==household_type_id))

    return result.scalars().all()



async def get_residents_by_age_groups(session: AsyncSession):
    model = AgeGroupsOfResidents
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_by_age_group(session: AsyncSession, age_group_id: int):
    model = AgeGroupsOfResidents
    result = await session.execute(select(model).filter(model.id==age_group_id))

    return result.scalars().all()



async def get_residents_non_germans(session: AsyncSession):
    model = NonGermanNationalsResidenceStatus
    result = await session.execute(select(model))

    return result.scalars().all()



async def get_residents_debt_counseling(session: AsyncSession):
    model = DebtCounselingOfResidents
    result = await session.execute(select(model))

    return result.scalars().all()



async def get_residents_education_support(session: AsyncSession):
    model = ChildEducationSupport
    result = await session.execute(select(model))

    return result.scalars().all()



async def get_residents(session: AsyncSession):
    model = ResidentsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = ResidentsByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_births(session: AsyncSession):
    model = BirthsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_births_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = BirthsByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_employed(session: AsyncSession):
    model = EmployedWithPensionInsuranceByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_employed_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = EmployedWithPensionInsuranceByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_ageratio(session: AsyncSession):
    model = AgeRatioByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_ageratio_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = AgeRatioByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_basicbenefits(session: AsyncSession):
    model = BasicBenefitsIncomeByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_basicbenefits_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = BasicBenefitsIncomeByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_ageunder18(session: AsyncSession):
    model = ChildrenAgeUnder18ByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_ageunder18_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = ChildrenAgeUnder18ByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_age18tounder65(session: AsyncSession):
    model = ResidentsAge18ToUnder65ByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_age18tounder65_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = ResidentsAge18ToUnder65ByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_age65andabove(session: AsyncSession):
    model = ResidentsAge65AndAboveByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_age65andabove_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = ResidentsAge65AndAboveByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_agegroups(session: AsyncSession):
    model = AgeGroupsOfResidentsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_agegroups_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = AgeGroupsOfResidentsByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_beneficiaries(session: AsyncSession):
    model = BeneficiariesByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()



async def get_residents_unemployed(session: AsyncSession):
    model = UnemployedResidentsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_unemployed_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = UnemployedResidentsByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_unemployed_by_categories(session: AsyncSession):
    model = UnemployedResidentsCategorizedByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_unemployed_by_categories_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = UnemployedResidentsCategorizedByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_beneficiaries_inactive(session: AsyncSession):
    model = InactiveBeneficiariesInHouseholdsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_beneficiaries_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = BeneficiariesByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_beneficiaries_characteristics(session: AsyncSession):
    model = BeneficiariesCharacteristicsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_beneficiaries_inactive_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = InactiveBeneficiariesInHouseholdsByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_beneficiaries_age15tounder65(session: AsyncSession):
    model = BeneficiariesAge15ToUnder65ByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_beneficiaries_age15tounder65_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = BeneficiariesAge15ToUnder65ByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_beneficiaries_characteristics_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = BeneficiariesCharacteristicsByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_migration_background(session: AsyncSession):
    model = MigrationBackgroundByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_migration_background_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = MigrationBackgroundByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_housing_assistance(session: AsyncSession):
    model = HousingAssistanceCasesByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_housing_assistance_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = HousingAssistanceCasesByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_housing_benefit(session: AsyncSession):
    model = HousingBenefitByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_housing_benefit_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = HousingBenefitByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()



async def get_residents_risk_homelessness(session: AsyncSession):
    model = HouseholdsRiskOfHomelessnessByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_risk_homelessness_by_district(session: AsyncSession, district_id: int):
    try:
        validated_district_id = validate_not_none(district_id)
        validated_district_id = validate_positive_int32(validated_district_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model = HouseholdsRiskOfHomelessnessByDistrict
    result = await session.execute(select(model).filter(model.district_id==validated_district_id))

    return result.scalars().all()
