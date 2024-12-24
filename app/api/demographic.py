from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dependencies import get_session
from ..service import (get_demographics_meta, get_district_details, get_districts, get_district, get_household_types, get_residents_by_age_groups, get_residents_non_germans, get_residents_debt_counseling, get_residents_education_support, get_residents, get_residents_by_district, get_residents_births, get_residents_births_by_district, get_residents_employed, get_residents_employed_by_district, get_residents_ageratio, get_residents_ageratio_by_district, get_residents_basicbenefits, get_residents_basicbenefits_by_district, get_residents_ageunder18, get_residents_ageunder18_by_district, get_residents_age18tounder65, get_residents_age18tounder65_by_district, get_residents_age65andabove, get_residents_age65andabove_by_district, get_residents_agegroups, get_residents_agegroups_by_district, get_residents_unemployed, get_residents_unemployed_by_district, get_residents_unemployed_by_categories, get_residents_unemployed_by_categories_by_district, get_residents_beneficiaries, get_residents_beneficiaries_by_district, get_residents_beneficiaries_inactive, get_residents_beneficiaries_inactive_by_district, get_residents_beneficiaries_characteristics, get_residents_beneficiaries_characteristics_by_district, get_residents_beneficiaries_age15tounder65, get_residents_beneficiaries_age15tounder65_by_district, get_residents_migration_background, get_residents_migration_background_by_district, get_residents_housing_assistance, get_residents_housing_assistance_by_district, get_residents_housing_benefit, get_residents_housing_benefit, get_residents_housing_benefit_by_district, get_residents_risk_homelessness, get_residents_risk_homelessness_by_district)
from ..schemas import (DistrictResponse, HouseholdTypeResponse, AgeGroupsOfResidentsResponse, NonGermanNationalsResidenceStatusResponse, DebtCounselingOfResidentsResponse, ChildEducationSupportResponse, ResidentsByDistrictResponse, BirthsByDistrictResponse, EmployedWithPensionInsuranceByDistrictResponse, AgeRatioByDistrictResponse, BasicBenefitsIncomeByDistrictResponse, ChildrenAgeUnder18ByDistrictResponse, ResidentsAge18ToUnder65ByDistrictResponse, ResidentsAge65AndAboveByDistrictResponse, AgeGroupsOfResidentsByDistrictResponse, UnemployedResidentsByDistrictResponse, UnemployedResidentsCategorizedByDistrictResponse, BeneficiariesByDistrictResponse, InactiveBeneficiariesInHouseholdsByDistrictResponse, BeneficiariesCharacteristicsByDistrictResponse, BeneficiariesAge15ToUnder65ByDistrictResponse, MigrationBackgroundByDistrictResponse, HousingAssistanceCasesByDistrictResponse, HousingBenefitByDistrictResponse, HouseholdsRiskOfHomelessnessByDistrictResponse)

route_demographic = APIRouter(prefix='/demographic/v1')


@route_demographic.get(
    '/meta',
    response_model=List,
    tags=['Sozialatlas']
)
async def fetch_demographics_meta(session: AsyncSession = Depends(get_session)):
    rows = await get_demographics_meta(session)
    result = jsonable_encoder(rows)

    return JSONResponse(content=result)



@route_demographic.get(
    '/details',
    response_model=List,
    tags=['Sozialatlas']
)
async def fetch_district_details(session: AsyncSession = Depends(get_session)):
    rows = await get_district_details(session)
    result = jsonable_encoder(rows)

    return JSONResponse(content=result[0])


@route_demographic.get(
    '/districts/',
    response_model=List[DistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_districts(session: AsyncSession = Depends(get_session)):
    rows = await get_districts(session)

    if len(rows) == 0:
        raise HTTPException(status_code=404, detail='Could not retrieve list of Flensburg districts')

    return rows 


@route_demographic.get(
    '/{district_id}',
    response_model=List[DistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_district(district_id: int, session: AsyncSession = Depends(get_session)):
    row = await get_district(session, district_id)
    schema = DistrictResponse

    try:
        return [schema(district_id=row.id, district_name=row.name)]
    except AttributeError as e:
        raise HTTPException(status_code=404, detail='Not found')



@route_demographic.get(
    '/household/types',
    response_model=List[HouseholdTypeResponse],
    tags=['Sozialatlas']
)
async def fetch_household_types(session: AsyncSession = Depends(get_session)):
    rows = await get_household_types(session)
    schema = HouseholdTypeResponse

    return [schema(household_id=r.id, household_type=r.label) for r in rows]


@route_demographic.get(
    '/residents/agegroups',
    response_model=List[AgeGroupsOfResidentsResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_by_age_groups(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_by_age_groups(session)
    schema = AgeGroupsOfResidentsResponse

    return [schema(year=r.year,
        age_under_18=r.age_under_18, age_18_to_under_30=r.age_18_to_under_30,
        age_30_to_under_45=r.age_30_to_under_45, age_45_to_under_65=r.age_45_to_under_65,
        age_65_to_under_80=r.age_65_to_under_80, age_80_and_above=r.age_80_and_above) for r in rows]


@route_demographic.get(
    '/residents/nongermans',
    response_model=List[NonGermanNationalsResidenceStatusResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_non_germans(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_non_germans(session)
    schema = NonGermanNationalsResidenceStatusResponse

    return [schema(year=r.year,
        permanent_residency=r.permanent_residency,
        permanent_residency_according_eu_freedom_movement_act=r.permanent_residency_according_eu_freedom_movement_act,
        permanent_residency_third_country_nationality=r.permanent_residency_third_country_nationality,
        without_permanent_residency=r.without_permanent_residency,
        asylum_seeker=r.asylum_seeker,
        suspension_of_deportation=r.suspension_of_deportation) for r in rows]


@route_demographic.get(
    '/residents/debtcounseling',
    response_model=List[DebtCounselingOfResidentsResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_debt_counseling(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_debt_counseling(session)
    schema = DebtCounselingOfResidentsResponse

    return [schema(year=r.year, household_type_id=r.household_type_id, residents=r.residents) for r in rows]


@route_demographic.get(
    '/residents/education/support',
    response_model=List[ChildEducationSupportResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_education_support(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_education_support(session)
    schema = ChildEducationSupportResponse

    return [schema(year=r.year,
        educational_assistance=r.educational_assistance,
        parenting_counselor=r.parenting_counselor,
        pedagogical_family_assistance=r.pedagogical_family_assistance,
        child_day_care_facility=r.child_day_care_facility,
        full_time_care=r.full_time_care,
        residential_education=r.residential_education,
        integration_assistance=r.integration_assistance,
        additional_support=r.additional_support) for r in rows]



@route_demographic.get(
    '/districts/residents',
    response_model=List[ResidentsByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents(session: AsyncSession = Depends(get_session)):
    rows = await get_residents(session)
    schema = ResidentsByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@route_demographic.get(
    '/{district_id}/residents',
    response_model=List[ResidentsByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_by_district(session, district_id)
    schema = ResidentsByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@route_demographic.get(
    '/districts/residents/births',
    response_model=List[BirthsByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_births(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_births(session)
    schema = BirthsByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        births=r.births,
        birth_rate=r.birth_rate) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/births',
    response_model=List[BirthsByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_births_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_births_by_district(session, district_id)
    schema = BirthsByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        births=r.births,
        birth_rate=r.birth_rate) for r in rows]


@route_demographic.get(
    '/districts/residents/employed',
    response_model=List[EmployedWithPensionInsuranceByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_employed(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_employed(session)
    schema = EmployedWithPensionInsuranceByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        residents=r.residents,
        employment_rate=r.employment_rate) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/employed',
    response_model=List[EmployedWithPensionInsuranceByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_employed_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_employed_by_district(session, district_id)
    schema = EmployedWithPensionInsuranceByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        residents=r.residents,
        employment_rate=r.employment_rate) for r in rows]



@route_demographic.get(
    '/districts/residents/ageratio',
    response_model=List[AgeRatioByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_ageratio(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_ageratio(session)
    schema = AgeRatioByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, quotient=r.quotient) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/ageratio',
    response_model=List[AgeRatioByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_ageratio_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_ageratio_by_district(session, district_id)
    schema = AgeRatioByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, quotient=r.quotient) for r in rows]



@route_demographic.get(
    '/districts/residents/basicbenefits',
    response_model=List[BasicBenefitsIncomeByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_basicbenefits(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_basicbenefits(session)
    schema = BasicBenefitsIncomeByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        male=r.male,
        female=r.female,
        age_18_to_under_65=r.age_18_to_under_65,
        age_65_and_above=r.age_65_and_above) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/basicbenefits',
    response_model=List[BasicBenefitsIncomeByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_basicbenefits_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_basicbenefits_by_district(session, district_id)
    schema = BasicBenefitsIncomeByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        male=r.male,
        female=r.female,
        age_18_to_under_65=r.age_18_to_under_65,
        age_65_and_above=r.age_65_and_above) for r in rows]



@route_demographic.get(
    '/districts/residents/ageunder18',
    response_model=List[ChildrenAgeUnder18ByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_ageunder18(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_ageunder18(session)
    schema = ChildrenAgeUnder18ByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/ageunder18',
    response_model=List[ChildrenAgeUnder18ByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_ageunder18_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_ageunder18_by_district(session, district_id)
    schema = ChildrenAgeUnder18ByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@route_demographic.get(
    '/districts/residents/age18tounder65',
    response_model=List[ResidentsAge18ToUnder65ByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_age18tounder65(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_age18tounder65(session)
    schema = ResidentsAge18ToUnder65ByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/age18tounder65',
    response_model=List[ResidentsAge18ToUnder65ByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_age18tounder65_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_age18tounder65_by_district(session, district_id)
    schema = ResidentsAge18ToUnder65ByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@route_demographic.get(
    '/districts/residents/age65andabove',
    response_model=List[ResidentsAge65AndAboveByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_age65andabove(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_age65andabove(session)
    schema = ResidentsAge65AndAboveByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/age65andabove',
    response_model=List[ResidentsAge65AndAboveByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_age65andabove_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_age65andabove_by_district(session, district_id)
    schema = ResidentsAge65AndAboveByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@route_demographic.get(
    '/districts/residents/agegroups',
    response_model=List[AgeGroupsOfResidentsByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_agegroups(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_agegroups(session)
    schema = AgeGroupsOfResidentsByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        age_under_18=r.age_under_18,
        age_18_to_under_30=r.age_18_to_under_30,
        age_30_to_under_45=r.age_30_to_under_45,
        age_45_to_under_65=r.age_45_to_under_65,
        age_65_to_under_80=r.age_65_to_under_80,
        age_80_and_above=r.age_80_and_above,
        age_0_to_under_7=r.age_0_to_under_7,
        age_60_and_above=r.age_60_and_above) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/agegroups',
    response_model=List[AgeGroupsOfResidentsByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_agegroups_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_agegroups_by_district(session, district_id)
    schema = AgeGroupsOfResidentsByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        age_under_18=r.age_under_18,
        age_18_to_under_30=r.age_18_to_under_30,
        age_30_to_under_45=r.age_30_to_under_45,
        age_45_to_under_65=r.age_45_to_under_65,
        age_65_to_under_80=r.age_65_to_under_80,
        age_80_and_above=r.age_80_and_above,
        age_0_to_under_7=r.age_0_to_under_7,
        age_60_and_above=r.age_60_and_above) for r in rows]



@route_demographic.get(
    '/districts/residents/unemployed',
    response_model=List[UnemployedResidentsByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_unemployed(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_unemployed(session)
    schema = UnemployedResidentsByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/unemployed',
    response_model=List[UnemployedResidentsByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_unemployed_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_unemployed_by_district(session, district_id)
    schema = UnemployedResidentsByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@route_demographic.get(
    '/districts/residents/unemployed/categorized',
    response_model=List[UnemployedResidentsCategorizedByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_unemployed_by_categories(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_unemployed_by_categories(session)
    schema = UnemployedResidentsCategorizedByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        unemployed_total=r.unemployed_total,
        percentage_of_total=r.percentage_of_total,
        percentage_sgb_iii=r.percentage_sgb_iii,
        percentage_sgb_ii=r.percentage_sgb_ii,
        percentage_foreign_citizenship=r.percentage_foreign_citizenship,
        percentage_female=r.percentage_female,
        percentage_age_under_25=r.percentage_age_under_25) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/unemployed/categorized',
    response_model=List[UnemployedResidentsCategorizedByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_unemployed_by_categories_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_unemployed_by_categories_by_district(session, district_id)
    schema = UnemployedResidentsCategorizedByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        unemployed_total=r.unemployed_total,
        percentage_of_total=r.percentage_of_total,
        percentage_sgb_iii=r.percentage_sgb_iii,
        percentage_sgb_ii=r.percentage_sgb_ii,
        percentage_foreign_citizenship=r.percentage_foreign_citizenship,
        percentage_female=r.percentage_female,
        percentage_age_under_25=r.percentage_age_under_25) for r in rows]



@route_demographic.get(
    '/districts/residents/beneficiaries',
    response_model=List[BeneficiariesByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_beneficiaries(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_beneficiaries(session)
    schema = BeneficiariesByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/beneficiaries',
    response_model=List[BeneficiariesByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_beneficiaries_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_beneficiaries_by_district(session, district_id)
    schema = BeneficiariesByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@route_demographic.get(
    '/districts/residents/beneficiaries/inactive',
    response_model=List[InactiveBeneficiariesInHouseholdsByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_beneficiaries_inactive(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_beneficiaries_inactive(session)
    schema = InactiveBeneficiariesInHouseholdsByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/beneficiaries/inactive',
    response_model=List[InactiveBeneficiariesInHouseholdsByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_beneficiaries_inactive_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_beneficiaries_inactive_by_district(session, district_id)
    schema = InactiveBeneficiariesInHouseholdsByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@route_demographic.get(
    '/districts/residents/beneficiaries/characteristics',
    response_model=List[BeneficiariesCharacteristicsByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_beneficiaries_by_characteristics(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_beneficiaries_characteristics(session)
    schema = BeneficiariesCharacteristicsByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        unemployability=r.unemployability,
        employability=r.employability,
        percentage_females=r.percentage_females,
        percentage_single_parents=r.percentage_single_parents,
        percentage_foreign_citizenship=r.percentage_foreign_citizenship) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/beneficiaries/characteristics',
    response_model=List[BeneficiariesCharacteristicsByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_beneficiaries_by_characteristics_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_beneficiaries_characteristics_by_district(session, district_id)
    schema = BeneficiariesCharacteristicsByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        unemployability=r.unemployability,
        employability=r.employability,
        percentage_females=r.percentage_females,
        percentage_single_parents=r.percentage_single_parents,
        percentage_foreign_citizenship=r.percentage_foreign_citizenship) for r in rows]



@route_demographic.get(
    '/districts/residents/beneficiaries/age15tounder65',
    response_model=List[BeneficiariesAge15ToUnder65ByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_beneficiaries_age15tounder65(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_beneficiaries_age15tounder65(session)
    schema = BeneficiariesAge15ToUnder65ByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        percentage_of_total_residents=r.percentage_of_total_residents,
        employable_with_benefits=r.employable_with_benefits,
        unemployment_benefits=r.unemployment_benefits,
        basic_income=r.basic_income,
        assisting_benefits=r.assisting_benefits) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/beneficiaries/age15tounder65',
    response_model=List[BeneficiariesAge15ToUnder65ByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_beneficiaries_age15tounder65_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_beneficiaries_age15tounder65_by_district(session, district_id)
    schema = BeneficiariesAge15ToUnder65ByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        percentage_of_total_residents=r.percentage_of_total_residents,
        employable_with_benefits=r.employable_with_benefits,
        unemployment_benefits=r.unemployment_benefits,
        basic_income=r.basic_income,
        assisting_benefits=r.assisting_benefits) for r in rows]



@route_demographic.get(
    '/districts/residents/migration/background',
    response_model=List[MigrationBackgroundByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_migration_background(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_migration_background(session)
    schema = MigrationBackgroundByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        foreign_citizenship=r.foreign_citizenship,
        german_citizenship=r.german_citizenship) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/migration/background',
    response_model=List[MigrationBackgroundByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_migration_background_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_migration_background_by_district(session, district_id)
    schema = MigrationBackgroundByDistrictResponse

    return [schema(year=r.year,
        district_id=r.district_id,
        foreign_citizenship=r.foreign_citizenship,
        german_citizenship=r.german_citizenship) for r in rows]



@route_demographic.get(
    '/districts/residents/housing/assistance',
    response_model=List[HousingAssistanceCasesByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_housing_assistance(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_housing_assistance(session)
    schema = HousingAssistanceCasesByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id,
        general_consulting=r.general_consulting,
        notices_of_rent_arrears=r.notices_of_rent_arrears,
        termination_rent_arrears=r.termination_rent_arrears,
        termination_for_conduct=r.termination_for_conduct,
        action_for_eviction=r.action_for_eviction,
        eviction_notice=r.eviction_notice,
        eviction_carried=r.eviction_carried) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/housing/assistance',
    response_model=List[HousingAssistanceCasesByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_housing_assistance_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_housing_assistance_by_district(session, district_id)
    schema = HousingAssistanceCasesByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id,
        general_consulting=r.general_consulting,
        notices_of_rent_arrears=r.notices_of_rent_arrears,
        termination_rent_arrears=r.termination_rent_arrears,
        termination_for_conduct=r.termination_for_conduct,
        action_for_eviction=r.action_for_eviction,
        eviction_notice=r.eviction_notice,
        eviction_carried=r.eviction_carried) for r in rows]



@route_demographic.get(
    '/districts/residents/housing/benefit',
    response_model=List[HousingBenefitByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_housing_benefit_by_district(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_housing_benefit(session)
    schema = HousingBenefitByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@route_demographic.get(
    '/districts/residents/housing/benefit',
    response_model=List[HousingBenefitByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_housing_benefit(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_housing_benefit(session)
    schema = HousingBenefitByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/housing/benefit',
    response_model=List[HousingBenefitByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_housing_benefit_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_housing_benefit_by_district(session, district_id)
    schema = HousingBenefitByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@route_demographic.get(
    '/districts/residents/risk/homelessness',
    response_model=List[HouseholdsRiskOfHomelessnessByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_risk_homelessness(session: AsyncSession = Depends(get_session)):
    rows = await get_residents_risk_homelessness(session)
    schema = HouseholdsRiskOfHomelessnessByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@route_demographic.get(
    '/{district_id}/residents/risk/homelessness',
    response_model=List[HouseholdsRiskOfHomelessnessByDistrictResponse],
    tags=['Sozialatlas']
)
async def fetch_residents_risk_homelessness_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await get_residents_risk_homelessness_by_district(session, district_id)
    schema = HouseholdsRiskOfHomelessnessByDistrictResponse

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



