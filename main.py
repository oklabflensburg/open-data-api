from fastapi import Depends, FastAPI, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import List

import base
import schemas
import service


app = FastAPI()
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



@router.get('/districts', response_model=list[schemas.District])
async def get_all_districts(session: AsyncSession = Depends(get_session)):
    districts = await service.get_districts(session)

    return [schemas.District(district_id=d.id, district_name=d.name) for d in districts]


'''
@router.get('/household/types', response_model=list[schemas.HouseholdType])
async def get_all_household_types(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/residents/agegroups', response_model=list[schemas.AgeGroupsOfResident])
async def get_all_residents/agegroups(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/residents/nongermans', response_model=list[schemas.NonGermanNationalsResidenceStatus])
async def get_all_residents_nongermans(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/residents/debtcounseling', response_model=list[schemas.DebtCounseling])
async def get_all_residents_debtcounseling(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/residents/education/support', response_model=list[schemas.ChildEducationSupport])
async def get_all_residents_education_support(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents', response_model=list[schemas.ResidentsByDistrict])
async def get_all_residents(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/births', response_model=list[schemas.BirthsByDistrict])
async def get_all_residents_births(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/employed', response_model=list[schemas.EmployedWithPensionInsuranceByDistrict])
async def get_all_residents_employed(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/ageratio', response_model=list[schemas.AgeRatioByDistrict])
async def get_all_residents_ageratio(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/basicbenefits', response_model=list[schemas.BasicBenefitsIncomeByDistrict])
async def get_all_residents_basicbenefits(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/ageunder18', response_model=list[schemas.ChildrenAgeUnder18ByDistrict])
async def get_all_residents_ageunder18(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/age18tounder65', response_model=list[schemas.ResidentsAge18ToUnder65ByDistrict])
async def get_all_residents_age18tounder65(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/age65andabove', response_model=list[schemas.ResidentsAge65AndAboveByDistrict])
async def get_all_residents_age65andabove(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/agegroups', response_model=list[schemas.AgeGroupsOfResidentsByDistrict])
async def get_all_residents_agegroups(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/unemployed', response_model=list[schemas.UnemployedResidentsByDistrict])
async def get_all_residents_unemployed(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/unemployed/categorized', response_model=list[schemas.UnemployedResidentsByDistrictsCategorized])
async def get_all_residents_unemployed_categorized(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/beneficiaries', response_model=list[schemas.BeneficiariesByDistrict])
async def get_all_residents_beneficiaries(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/beneficiaries/inactive', response_model=list[schemas.InactiveBeneficiariesInHouseholdsByDistrict])
async def get_all_residents_beneficiaries_inactive(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/beneficiaries/characteristics', response_model=list[schemas.BeneficiariesCharacteristicsByDistrict])
async def get_all_residents_beneficiaries_characteristics(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/beneficiaries/age15tounder65', response_model=list[schemas.BeneficiariesAge15ToUnder65ByDistrict])
async def get_all_residents_beneficiaries_age15tounder65(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/migration/background', response_model=list[schemas.MigrationBackgroundByDistrict])
async def get_all_residents_migration_background(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/housing/assistance', response_model=list[schemas.HousingAssistanceCasesByDistrict])
async def get_all_districts_residents_housing_assistance(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/housing/benefit', response_model=list[schemas.HousingBenefitByDistrict])
async def get_all_residents_housing_benefit(session: AsyncSession = Depends(get_session)):
    pass


@router.get('/district/residents/risk/homelessness', response_model=list[schemas.HouseholdsAtRiskOfHomelessnessByDistrict])
async def get_all_residents_risk_homelessness(session: AsyncSession = Depends(get_session)):
    pass
'''

app.include_router(router)
