from fastapi import Depends, FastAPI, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import List

import base
import schemas
import service


app = FastAPI(title='Sozialatlas', summary='Some endpoints are not yet implemented')
Base = declarative_base()
router = APIRouter(prefix='/sozialatlas/v1')


@app.on_event('startup')
async def init_schemas():
    async with base.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Dependency
async def get_session() -> AsyncSession:
    async with base.async_session() as session:
        yield session



@router.get('/{district_id}', response_model=list[schemas.District])
async def get_district(district_id: int, session: AsyncSession = Depends(get_session)):
    row = await service.get_district(session, district_id)
    schema = schemas.District

    try:
        return [schema(district_id=row.id, district_name=row.name)]
    except AttributeError as e:
        raise HTTPException(status_code=404, detail='Not found')


@router.get('/districts/', response_model=list[schemas.District], tags=['districts'])
async def get_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_districts(session)
    schema = schemas.District

    return [schema(district_id=r.id, district_name=r.name) for r in rows]


@router.get('/household/types', response_model=list[schemas.HouseholdType])
async def get_household_types(session: AsyncSession = Depends(get_session)):
    rows = await service.get_household_types(session)
    schema = schemas.HouseholdTypes

    return [schema(household_id=r.id, household_type=r.label) for r in rows]


@router.get('/residents/agegroups', response_model=list[schemas.AgeGroupsOfResidents])
async def get_residents_by_age_groups(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_by_age_groups(session)
    schema = schemas.AgeGroupsOfResidents

    return [schema(year=r.year,
        age_under_18=r.age_under_18, age_18_to_under_30=r.age_18_to_under_30,
        age_30_to_under_45=r.age_30_to_under_45, age_45_to_under_65=r.age_45_to_under_65,
        age_65_to_under_80=r.age_65_to_under_80, age_80_and_above=r.age_80_and_above) for r in rows]


@router.get('/residents/nongermans', response_model=list[schemas.NonGermanNationalsResidenceStatus])
async def get_residents_non_germans(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_non_germans(session)
    schema = schemas.NonGermanNationalsResidenceStatus

    return [schema(year=r.year,
        permanent_residency=r.permanent_residency,
        permanent_residency_according_eu_freedom_movement_act=r.permanent_residency_according_eu_freedom_movement_act,
        permanent_residency_third_country_nationality=r.permanent_residency_third_country_nationality,
        without_permanent_residency=r.without_permanent_residency,
        asylum_seeker=r.asylum_seeker,
        suspension_of_deportation=r.suspension_of_deportation) for r in rows]


@router.get('/residents/debtcounseling', response_model=list[schemas.DebtCounselingOfResidents])
async def get_residents_debt_counseling(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_debt_counseling(session)
    schema = schemas.DebtCounselingOfResidents

    return [schema(year=r.year, household_type_id=r.household_type_id, residents=r.residents) for r in rows]


@router.get('/residents/education/support', response_model=list[schemas.ChildEducationSupport])
async def get_residents_education_support(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_education_support(session)
    schema = schemas.ChildEducationSupport

    return [schema(year=r.year,
        educational_assistance=r.educational_assistance,
        parenting_counselor=r.parenting_counselor,
        pedagogical_family_assistance=r.pedagogical_family_assistance,
        child_day_care_facility=r.child_day_care_facility,
        full_time_care=r.full_time_care,
        residential_education=r.residential_education,
        integration_assistance=r.integration_assistance,
        additional_support=r.additional_support) for r in rows]


@router.get('/{district_id}/residents', response_model=list[schemas.ResidentsByDistrict])
async def get_residents_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_by_district(session, district_id)
    schema = schemas.ResidentsByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router.get('/{district_id}/residents/births', response_model=list[schemas.BirthsByDistrict])
async def get_residents_births_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_births_by_district(session, district_id)
    schema = schemas.BirthsByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        births=r.births,
        birth_rate=r.birth_rate) for r in rows]


@router.get('/{district_id}/residents/employed', response_model=list[schemas.EmployedWithPensionInsuranceByDistrict])
async def get_residents_employed_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_employed_by_district(session, district_id)
    schema = schemas.EmployedWithPensionInsuranceByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        residents=r.residents,
        employment_rate=r.employment_rate) for r in rows]


@router.get('/{district_id}/residents/ageratio', response_model=list[schemas.AgeRatioByDistrict])
async def get_residents_ageratio_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_ageratio_by_district(session, district_id)
    schema = schemas.AgeRatioByDistrict

    return [schema(year=r.year, district_id=r.district_id, quotient=r.quotient) for r in rows]


@router.get('/{district_id}/residents/basicbenefits', response_model=list[schemas.BasicBenefitsIncomeByDistrict])
async def get_residents_basicbenefits_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_basicbenefits_by_district(session, district_id)
    schema = schemas.BasicBenefitsIncomeByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        male=r.male,
        female=r.female,
        age_18_to_under_65=r.age_18_to_under_65,
        age_65_and_above=r.age_65_and_above) for r in rows]


@router.get('/{district_id}/residents/ageunder18', response_model=list[schemas.ChildrenAgeUnder18ByDistrict])
async def get_residents_ageunder18_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_ageunder18_by_district(session, district_id)
    schema = schemas.ChildrenAgeUnder18ByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router.get('/{district_id}/residents/age18tounder65', response_model=list[schemas.ResidentsAge18ToUnder65ByDistrict])
async def get_residents_age18tounder65_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_age18tounder65_by_district(session, district_id)
    schema = schemas.ResidentsAge18ToUnder65ByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router.get('/{district_id}/residents/age65andabove', response_model=list[schemas.ResidentsAge65AndAboveByDistrict])
async def get_residents_age65andabove_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_age65andabove_by_district(session, district_id)
    schema = schemas.ResidentsAge65AndAboveByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router.get('/{district_id}/residents/agegroups', response_model=list[schemas.AgeGroupsOfResidentsByDistrict])
async def get_residents_agegroups_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_agegroups_by_district(session, district_id)
    schema = schemas.AgeGroupsOfResidentsByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        age_under_18=r.age_under_18,
        age_18_to_under_30=r.age_18_to_under_30,
        age_30_to_under_45=r.age_30_to_under_45,
        age_45_to_under_65=r.age_45_to_under_65,
        age_65_to_under_80=r.age_65_to_under_80,
        age_80_and_above=r.age_80_and_older,
        age_0_to_under_7=r.age_0_to_under_7,
        age_60_and_above=r.age_60_and_older) for r in rows]


@router.get('/{district_id}/residents/unemployed', response_model=list[schemas.UnemployedResidentsByDistrict])
async def get_residents_unemployed_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_unemployed_by_district(session, district_id)
    schema = schemas.UnemployedResidentsByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router.get('/{district_id}/residents/unemployed/categorized', response_model=list[schemas.UnemployedCategorizedResidentsByDistrict])
async def get_residents_unemployed_by_categories_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_unemployed_categorized_by_district(session, district_id)
    schema = schemas.UnemployedCategorizedResidentsByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        unemployed_total=r.unemployed_total,
        percentage_of_total=r.percentage_of_total,
        percentage_sgb_iii=r.percentage_sgb_iii,
        percentage_sgb_ii=r.percentage_sgb_ii,
        percentage_foreign_citizenship=r.percentage_foreign_citizenship,
        percentage_female=r.percentage_female,
        percentage_age_under_25=r.percentage_age_under_25) for r in rows]


@router.get('/{district_id}/residents/beneficiaries', response_model=list[schemas.BeneficiariesByDistrict])
async def get_residents_beneficiaries_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_beneficiaries_by_district(session, district_id)
    schema = schemas.BeneficiariesByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router.get('/{district_id}/residents/beneficiaries/inactive', response_model=list[schemas.InactiveBeneficiariesInHouseholdsByDistrict])
async def get_residents_beneficiaries_inactive_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_beneficiaries_inactive_by_district(session, district_id)
    schema = schemas.InactiveBeneficiariesInHouseholdsByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router.get('/districts/residents/beneficiaries/characteristics', response_model=list[schemas.BeneficiariesCharacteristicsByDistrict])
async def get_residents_beneficiaries_by_characteristics_by_districts(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_beneficiaries_characteristics_by_districts(session)
    schema = schemas.BeneficiariesCharacteristicsByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        unemployability=r.unemployability,
        employability=r.employability,
        percentage_females=r.percentage_females,
        percentage_single_parents=r.percenatage_single_parents,
        percentage_foreign_citizenship=r.percentage_foreign_citizenship) for r in rows]


@router.get('/{district_id}/residents/beneficiaries/age15tounder65', response_model=list[schemas.BeneficiariesAge15ToUnder65ByDistrict])
async def get_residents_beneficiaries_age15tounder65_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_beneficiaries_age15tounder65_by_district(session, district_id)
    schema = schemas.BeneficiariesAge15ToUnder65ByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        percentage_of_total_residents=r.percentage_of_total_residents,
        employable_with_benefits=r.employable_with_benefits,
        unemployment_benefits=r.unemployment_benefits,
        basic_income=r.basic_income,
        assisting_benefits=r.assisting_benefits) for r in rows]



@router.get('/{district_id}/residents/migration/background', response_model=list[schemas.MigrationBackgroundByDistrict])
async def get_residents_migration_background_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_migration_background_by_district(session, district_id)
    schema = schemas.MigrationBackgroundByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        foreign_citizenship=r.foreign_citizenship,
        german_citizenship=r.german_citizenship) for r in rows]


@router.get('/districts/residents/housing/assistance', response_model=list[schemas.HousingAssistanceCasesByDistrict])
async def get_residents_housing_assistance_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_housing_assistance_by_districts(session)
    schema = schemas.HousingAssistanceCasesByDistrict

    return [schema(year=r.year, district_id=r.district_id,
        general_consulting=r.general_consulting,
        notices_of_rent_arrears=r.notices_of_rent_arrears,
        termination_rent_arrears=r.termination_rent_arrears,
        termination_for_conduct=r.termination_for_conduct,
        action_for_eviction=r.action_for_eviction,
        eviction_notice=r.eviction_notice,
        eviction_carried=r.eviction_carried) for r in rows]


@router.get('/{district_id}/residents/housing/assistance', response_model=list[schemas.HousingAssistanceCasesByDistrict])
async def get_residents_housing_assistance_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_housing_assistance_by_district(session, district_id)
    schema = schemas.HousingAssistanceCasesByDistrict

    return [schema(year=r.year, district_id=r.district_id,
        general_consulting=r.general_consulting,
        notices_of_rent_arrears=r.notices_of_rent_arrears,
        termination_rent_arrears=r.termination_rent_arrears,
        termination_for_conduct=r.termination_for_conduct,
        action_for_eviction=r.action_for_eviction,
        eviction_notice=r.eviction_notice,
        eviction_carried=r.eviction_carried) for r in rows]



@router.get('/districts/residents/housing/benefit', response_model=list[schemas.HousingBenefitByDistrict])
async def get_residents_housing_benefit_by_district(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_housing_benefit_by_districts(session)
    schema = schemas.HousingBenefitByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@router.get('/districts/residents/housing/benefit', response_model=list[schemas.HousingBenefitByDistrict])
async def get_residents_housing_benefit_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_housing_benefit_by_districts(session)
    schema = schemas.HousingBenefitByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router.get('/{district_id}/residents/housing/benefit', response_model=list[schemas.HousingBenefitByDistrict])
async def get_residents_housing_benefit_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_housing_benefit_by_district(session, district_id)
    schema = schemas.HousingBenefitByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@router.get('/districts/residents/risk/homelessness',
        response_model=list[schemas.HouseholdsAtRiskOfHomelessnessByDistricts])
async def get_residents_risk_homelessness_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_risk_homelessness_by_districts(session)
    schema = schemas.HouseholdsAtRiskOfHomelessnessByDistricts

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router.get('/{district_id}/residents/risk/homelessness', response_model=list[schemas.HouseholdsAtRiskOfHomelessnessByDistrict])
async def get_residents_risk_homelessness_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_risk_homelessness_by_district(session, district_id)
    schema = schemas.HouseholdsAtRiskOfHomelessnessByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


app.include_router(router)
