from fastapi import Request, Depends, FastAPI, APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import List

import json

import base
import schemas
import service


app = FastAPI(docs_url=None, redoc_url=None, version='1.17', title='Opendata API', summary='Some endpoints are not yet implemented')
Base = declarative_base()

router1 = APIRouter(prefix='/demographics/v1')
router2 = APIRouter(prefix='/accidents/v1')
router3 = APIRouter(prefix='/monuments/v1')
router4 = APIRouter(prefix='/biotope/v1')
router5 = APIRouter(prefix='/administrative/v1')
router6 = APIRouter(prefix='/energy/v1')


app.mount('/static', StaticFiles(directory='static'), name='static')



@app.on_event('startup')
async def init_schemas():
    async with base.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Dependency
async def get_session() -> AsyncSession:
    async with base.async_session() as session:
        yield session


@app.get('/', include_in_schema=False)
def home_redirect():
    return RedirectResponse('/docs')


@app.get('/docs', include_in_schema=False)
async def swagger_ui_html(req: Request) -> HTMLResponse:
    return get_swagger_ui_html(
        title=app.title,
        openapi_url='/openapi.json',
        swagger_favicon_url='/static/favicon.ico'
    )



@router6.get(
    '/meta/state',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of German states with corresponding ids.')
)
async def get_energy_state_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_energy_state_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Could not retrieve list of German state codes')


@router6.get(
    '/meta/country',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of countries provided by the German market master data register.')
)
async def get_energy_country_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_energy_country_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Could not retrieve list of country codes')


@router6.get(
    '/meta/audit',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of network operator audit codes provided by the German market master data register')
)
async def get_network_operator_audit_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_network_operator_audit_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Could not retrieves list of network operator audit codes')


@router6.get(
    '/meta/location',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of energy location codes')
)
async def get_energy_location_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_energy_location_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Could not retrieve list of energy location codes')


@router6.get(
    '/meta/supply/type',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of energy supply types')
)
async def get_energy_supply_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_energy_supply_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Could not retrieves a list of energy supply types')


@router6.get(
    '/meta/source/type',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of energy source types')
)
async def get_energy_source_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_energy_source_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Could not retrieves list of energy source types')


@router6.get(
    '/meta/manufacturer',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of turbine manufacturers.')
)
async def get_turbine_manufacturer_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_turbine_manufacturer_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Turbine manufacturer not found')


@router6.get(
    '/meta/power/limitation',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of power limitations.')
)
async def get_power_limitation_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_power_limitation_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Power limitation not found')


@router6.get(
    '/meta/power/technology',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of power technologies.')
)
async def get_power_technology_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_power_technology_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Power technology not found')


@router6.get(
    '/meta/orientation',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of main orientations.')
)
async def get_main_orientation_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_main_orientation_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Main orientation not found')


@router6.get(
    '/meta/orientation/angle',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of orientation tilt angles.')
)
async def get_orientation_tilt_angle_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_orientation_tilt_angle_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Orientation tilt angle not found')


@router6.get(
    '/meta/usage/area',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of usage areas.')
)
async def get_usage_area_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_usage_area_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Usage area not found')


@router6.get(
    '/meta/operational/status',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of operational statuses.')
)
async def get_operational_status_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_operational_status_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Operational status not found')


@router6.get(
    '/meta/biomass/type',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of biomass types.')
)
async def get_biomass_type_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_biomass_type_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Biomass type not found')


@router6.get(
    '/meta/primary/fuel',
    response_model=list,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of primary fuels.')
)
async def get_primary_fuel_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_primary_fuel_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Primary fuel not found')



@router6.get(
    '/unit/combustion/id',
    response_model=list,
    tags=['Marktstammdatenregister Combustion'],
    description=('Retrieves details about a specific combustion unit based on the provided 15 digit unit registration number.')
)
async def get_combustion_unit_by_id(
    unit_id: str = Query(None, min_length=15, max_length=15),
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_combustion_unit_by_id(session, unit_id)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'Combustion unit with id "{unit_id}" not found')


@router6.get(
    '/unit/combustion/key',
    response_model=list,
    tags=['Marktstammdatenregister Combustion'],
    description=('Retrieves a list of combustion units with each detail based on the provided German municipality key (AGS).')
)
async def get_combustion_unit_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_combustion_unit_by_municipality_key(session, municipality_key)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No combustion units for municipality key {municipality_key} found')

    return JSONResponse(content=response)



@router6.get(
    '/unit/nuclear/id',
    response_model=list,
    tags=['Marktstammdatenregister Nuclear'],
    description=('Retrieves details about a specific nuclear unit based on the provided 15 digit unit registration number.')
)
async def get_nuclear_unit_by_id(
    unit_id: str = Query(None, min_length=15, max_length=15),
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_nuclear_unit_by_id(session, unit_id)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'Nuclear unit with id "{unit_id}" not found')


@router6.get(
    '/unit/nuclear/key',
    response_model=list,
    tags=['Marktstammdatenregister Nuclear'],
    description=('Retrieves a list of nuclear units with each detail based on the provided German municipality key (AGS).')
)
async def get_nuclear_unit_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_nuclear_unit_by_municipality_key(session, municipality_key)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No nuclear units for municipality key {municipality_key} found')

    return JSONResponse(content=response)



@router6.get(
    '/unit/water/id',
    response_model=list,
    tags=['Marktstammdatenregister Water'],
    description=('Retrieves details about a specific water unit based on the provided 15 digit unit registration number.')
)
async def get_water_unit_by_id(
    unit_id: str = Query(None, min_length=15, max_length=15),
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_water_unit_by_id(session, unit_id)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'Water unit with id "{unit_id}" not found')


@router6.get(
    '/unit/water/key',
    response_model=list,
    tags=['Marktstammdatenregister Water'],
    description=('Retrieves a list of water units with each detail based on the provided German municipality key (AGS).')
)
async def get_water_unit_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_water_unit_by_municipality_key(session, municipality_key)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No water units for municipality key {municipality_key} found')

    return JSONResponse(content=response)



@router6.get(
    '/unit/biomass/id',
    response_model=list,
    tags=['Marktstammdatenregister Biomass'],
    description=('Retrieves details about a specific biomass unit based on the provided 15 digit unit registration number.')
)
async def get_biomass_unit_by_id(
    unit_id: str = Query(None, min_length=15, max_length=15),
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_biomass_unit_by_id(session, unit_id)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'Biomass unit with id "{unit_id}" not found')


@router6.get(
    '/unit/biomass/key',
    response_model=list,
    tags=['Marktstammdatenregister Biomass'],
    description=('Retrieves a list of biomass units with each details based on the provided german municipality key (AGS).')
)
async def get_biomass_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_biomass_unit_by_municipality_key(session, municipality_key)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No biomass units for municipality key {municipality_key} found')

    return JSONResponse(content=response)



@router6.get(
    '/unit/wind/id',
    response_model=list,
    tags=['Marktstammdatenregister Wind'],
    description=('Retrieves details about a specific wind turbine unit based on the provided 15 digit unit registration number.')
)
async def get_wind_unit_by_id(
    unit_id: str = Query(None, min_length=15, max_length=15),
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_wind_unit_by_id(session, unit_id)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'Wind turbine unit with id "{unit_id}" not found')


@router6.get(
    '/unit/wind/key',
    response_model=list,
    tags=['Marktstammdatenregister Wind'],
    description=('Retrieves a list of wind turbine units with each details based on the provided german municipality key (AGS).')
)
async def get_wind_unit_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_wind_unit_by_municipality_key(session, municipality_key)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No wind turbine units for municipality key {municipality_key} found')

    return JSONResponse(content=response)



@router6.get(
    '/unit/solar/id',
    response_model=list,
    tags=['Marktstammdatenregister Solar'],
    description=('Retrieves the solar unit details based on the provided 15 digit unit registration number.')
)
async def get_solar_unit_by_id(
    unit_id: str = Query(None, min_length=15, max_length=15),
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_solar_unit_by_id(session, unit_id)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'Solar unit with id "{unit_id}" not found')


@router6.get(
    '/unit/solar/key',
    response_model=list,
    tags=['Marktstammdatenregister Solar'],
    description=('Retrieves a list of solar units with each details based on the provided german municipality key (AGS).')
)
async def get_solar_unit_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_solar_unit_by_municipality_key(session, municipality_key)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No solar units for municipality key {municipality_key} found')

    return JSONResponse(content=response)



@router5.get('/parcel', response_model=list, tags=['Verwaltungsgebiete'])
async def get_parcel_meta_by_lat_lng(lat: float, lng: float, session: AsyncSession = Depends(get_session)):
    rows = await service.get_parcel_meta_by_lat_lng(session, lat, lng)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Not found')


@router5.get(
    '/municipality/search',
    response_model=list,
    tags=['Verwaltungsgebiete'],
    description=('Retrieves municipality name and key as well as the region name based on the provided query.')
)
async def get_municipality_by_query(
    query: str = Query(None, min_length=2),
    session: AsyncSession = Depends(get_session)
):
    rows = await service.get_municipality_by_query(session, query)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'no results found')


@router5.get(
    '/municipality',
    response_model=list,
    tags=['Verwaltungsgebiete'],
    description=('Retrieves the geometry, bounding box, shape area, and statistical information of a municipality based on the provided municipality key (AGS) or the municipality name.')
)
async def get_municipality(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    municipality_name: str = Query(None, min_length=2),
    session: AsyncSession = Depends(get_session)
):
    if municipality_key:
        rows = await service.get_municipality_by_key(session, municipality_key)
        response = jsonable_encoder(rows)

        if len(response) == 0:
            raise HTTPException(status_code=404, detail='No municipality was found')

        return JSONResponse(content=response)
    elif municipality_name:
        rows = await service.get_municipality_by_name(session, municipality_name)
        response = jsonable_encoder(rows)

        if len(response) == 0:
            raise HTTPException(status_code=404, detail='No municipality was found')

        return JSONResponse(content=response)
    else:
        raise HTTPException(status_code=400, detail='Either "key" or "name" parameter must be provided')



@router4.get('/point', response_model=list, tags=['Biotopkartierung'])
async def get_biotope_meta_by_lat_lng(lat: float, lng: float, session: AsyncSession = Depends(get_session)):
    rows = await service.get_biotope_meta_by_lat_lng(session, lat, lng)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Not found')


@router4.get('/origin', response_model=list, tags=['Biotopkartierung'])
async def get_biotope_origin(code: str, session: AsyncSession = Depends(get_session)):
    rows = await service.get_biotope_origin(session, code)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Not found')



@router3.get('/details', response_model=list, tags=['Denkmalschutzliste'])
async def get_monuments(object_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_monuments(session, object_id)
    monuments = jsonable_encoder(rows)

    return JSONResponse(content=monuments[0])



@router2.get('/meta', response_model=list, tags=['Unfallatlas'])
async def get_accident_meta(session: AsyncSession = Depends(get_session)):
    rows = await service.get_accident_meta(session)
    result =jsonable_encoder(rows)

    return JSONResponse(content=result[0])


@router2.get('/details', response_model=list, tags=['Unfallatlas'])
async def get_accident_details_by_city(query: str, session: AsyncSession = Depends(get_session)):
    rows = await service.get_accident_details_by_city(session, query)
    result =jsonable_encoder(rows)

    return JSONResponse(content=result[0])



@router1.get('/meta', response_model=list, tags=['Sozialatlas'])
async def get_demographics_meta(session: AsyncSession = Depends(get_session)):
    rows = await service.get_demographics_meta(session)
    result =jsonable_encoder(rows)

    return JSONResponse(content=result)



@router1.get('/details', response_model=list, tags=['Sozialatlas'])
async def get_district_details(session: AsyncSession = Depends(get_session)):
    rows = await service.get_district_details(session)
    schema = schemas.DistrictDetails
    result =jsonable_encoder(rows)

    return JSONResponse(content=result[0])


@router1.get('/districts/', response_model=list[schemas.District], tags=['Sozialatlas'])
async def get_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_districts(session)
    schema = schemas.District

    return [schema(district_id=r.id, district_name=r.name) for r in rows]


@router1.get('/{district_id}', response_model=list[schemas.District], tags=['Sozialatlas'])
async def get_district(district_id: int, session: AsyncSession = Depends(get_session)):
    row = await service.get_district(session, district_id)
    schema = schemas.District

    try:
        return [schema(district_id=row.id, district_name=row.name)]
    except AttributeError as e:
        raise HTTPException(status_code=404, detail='Not found')



@router1.get('/household/types', response_model=list[schemas.HouseholdType], tags=['Sozialatlas'])
async def get_household_types(session: AsyncSession = Depends(get_session)):
    rows = await service.get_household_types(session)
    schema = schemas.HouseholdTypes

    return [schema(household_id=r.id, household_type=r.label) for r in rows]


@router1.get('/residents/agegroups', response_model=list[schemas.AgeGroupsOfResidents], tags=['Sozialatlas'])
async def get_residents_by_age_groups(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_by_age_groups(session)
    schema = schemas.AgeGroupsOfResidents

    return [schema(year=r.year,
        age_under_18=r.age_under_18, age_18_to_under_30=r.age_18_to_under_30,
        age_30_to_under_45=r.age_30_to_under_45, age_45_to_under_65=r.age_45_to_under_65,
        age_65_to_under_80=r.age_65_to_under_80, age_80_and_above=r.age_80_and_above) for r in rows]


@router1.get('/residents/nongermans', response_model=list[schemas.NonGermanNationalsResidenceStatus], tags=['Sozialatlas'])
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


@router1.get('/residents/debtcounseling', response_model=list[schemas.DebtCounselingOfResidents], tags=['Sozialatlas'])
async def get_residents_debt_counseling(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_debt_counseling(session)
    schema = schemas.DebtCounselingOfResidents

    return [schema(year=r.year, household_type_id=r.household_type_id, residents=r.residents) for r in rows]


@router1.get('/residents/education/support', response_model=list[schemas.ChildEducationSupport], tags=['Sozialatlas'])
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



@router1.get('/districts/residents', response_model=list[schemas.ResidentsByDistrict], tags=['Sozialatlas'])
async def get_residents_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_by_districts(session)
    schema = schemas.ResidentsByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router1.get('/{district_id}/residents', response_model=list[schemas.ResidentsByDistrict], tags=['Sozialatlas'])
async def get_residents_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_by_district(session, district_id)
    schema = schemas.ResidentsByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@router1.get('/districts/residents/births', response_model=list[schemas.BirthsByDistrict], tags=['Sozialatlas'])
async def get_residents_births_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_births_by_districts(session)
    schema = schemas.BirthsByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        births=r.births,
        birth_rate=r.birth_rate) for r in rows]


@router1.get('/{district_id}/residents/births', response_model=list[schemas.BirthsByDistrict], tags=['Sozialatlas'])
async def get_residents_births_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_births_by_district(session, district_id)
    schema = schemas.BirthsByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        births=r.births,
        birth_rate=r.birth_rate) for r in rows]


@router1.get('/districts/residents/employed', response_model=list[schemas.EmployedWithPensionInsuranceByDistrict], tags=['Sozialatlas'])
async def get_residents_employed_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_employed_by_districts(session)
    schema = schemas.EmployedWithPensionInsuranceByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        residents=r.residents,
        employment_rate=r.employment_rate) for r in rows]


@router1.get('/{district_id}/residents/employed', response_model=list[schemas.EmployedWithPensionInsuranceByDistrict], tags=['Sozialatlas'])
async def get_residents_employed_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_employed_by_district(session, district_id)
    schema = schemas.EmployedWithPensionInsuranceByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        residents=r.residents,
        employment_rate=r.employment_rate) for r in rows]



@router1.get('/districts/residents/ageratio', response_model=list[schemas.AgeRatioByDistrict], tags=['Sozialatlas'])
async def get_residents_ageratio_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_ageratio_by_districts(session)
    schema = schemas.AgeRatioByDistrict

    return [schema(year=r.year, district_id=r.district_id, quotient=r.quotient) for r in rows]


@router1.get('/{district_id}/residents/ageratio', response_model=list[schemas.AgeRatioByDistrict], tags=['Sozialatlas'])
async def get_residents_ageratio_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_ageratio_by_district(session, district_id)
    schema = schemas.AgeRatioByDistrict

    return [schema(year=r.year, district_id=r.district_id, quotient=r.quotient) for r in rows]



@router1.get('/districts/residents/basicbenefits', response_model=list[schemas.BasicBenefitsIncomeByDistrict], tags=['Sozialatlas'])
async def get_residents_basicbenefits_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_basicbenefits_by_districts(session)
    schema = schemas.BasicBenefitsIncomeByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        male=r.male,
        female=r.female,
        age_18_to_under_65=r.age_18_to_under_65,
        age_65_and_above=r.age_65_and_above) for r in rows]


@router1.get('/{district_id}/residents/basicbenefits', response_model=list[schemas.BasicBenefitsIncomeByDistrict], tags=['Sozialatlas'])
async def get_residents_basicbenefits_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_basicbenefits_by_district(session, district_id)
    schema = schemas.BasicBenefitsIncomeByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        male=r.male,
        female=r.female,
        age_18_to_under_65=r.age_18_to_under_65,
        age_65_and_above=r.age_65_and_above) for r in rows]



@router1.get('/districts/residents/ageunder18', response_model=list[schemas.ChildrenAgeUnder18ByDistrict], tags=['Sozialatlas'])
async def get_residents_ageunder18_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_ageunder18_by_districts(session)
    schema = schemas.ChildrenAgeUnder18ByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router1.get('/{district_id}/residents/ageunder18', response_model=list[schemas.ChildrenAgeUnder18ByDistrict], tags=['Sozialatlas'])
async def get_residents_ageunder18_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_ageunder18_by_district(session, district_id)
    schema = schemas.ChildrenAgeUnder18ByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@router1.get('/districts/residents/age18tounder65', response_model=list[schemas.ResidentsAge18ToUnder65ByDistrict], tags=['Sozialatlas'])
async def get_residents_age18tounder65_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_age18tounder65_by_districts(session)
    schema = schemas.ResidentsAge18ToUnder65ByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router1.get('/{district_id}/residents/age18tounder65', response_model=list[schemas.ResidentsAge18ToUnder65ByDistrict], tags=['Sozialatlas'])
async def get_residents_age18tounder65_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_age18tounder65_by_district(session, district_id)
    schema = schemas.ResidentsAge18ToUnder65ByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@router1.get('/districts/residents/age65andabove', response_model=list[schemas.ResidentsAge65AndAboveByDistrict], tags=['Sozialatlas'])
async def get_residents_age65andabove_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_age65andabove_by_districts(session)
    schema = schemas.ResidentsAge65AndAboveByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router1.get('/{district_id}/residents/age65andabove', response_model=list[schemas.ResidentsAge65AndAboveByDistrict], tags=['Sozialatlas'])
async def get_residents_age65andabove_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_age65andabove_by_district(session, district_id)
    schema = schemas.ResidentsAge65AndAboveByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@router1.get('/districts/residents/agegroups', response_model=list[schemas.AgeGroupsOfResidentsByDistrict], tags=['Sozialatlas'])
async def get_residents_agegroups_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_agegroups_by_districts(session)
    schema = schemas.AgeGroupsOfResidentsByDistrict

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


@router1.get('/{district_id}/residents/agegroups', response_model=list[schemas.AgeGroupsOfResidentsByDistrict], tags=['Sozialatlas'])
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
        age_80_and_above=r.age_80_and_above,
        age_0_to_under_7=r.age_0_to_under_7,
        age_60_and_above=r.age_60_and_above) for r in rows]



@router1.get('/districts/residents/unemployed', response_model=list[schemas.UnemployedResidentsByDistrict], tags=['Sozialatlas'])
async def get_residents_unemployed_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_unemployed_by_districts(session)
    schema = schemas.UnemployedResidentsByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router1.get('/{district_id}/residents/unemployed', response_model=list[schemas.UnemployedResidentsByDistrict], tags=['Sozialatlas'])
async def get_residents_unemployed_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_unemployed_by_district(session, district_id)
    schema = schemas.UnemployedResidentsByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@router1.get('/districts/residents/unemployed/categorized', response_model=list[schemas.UnemployedCategorizedResidentsByDistrict], tags=['Sozialatlas'])
async def get_residents_unemployed_by_categories_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_unemployed_by_categories_by_districts(session)
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


@router1.get('/{district_id}/residents/unemployed/categorized', response_model=list[schemas.UnemployedCategorizedResidentsByDistrict], tags=['Sozialatlas'])
async def get_residents_unemployed_by_categories_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_unemployed_by_categories_by_district(session, district_id)
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



@router1.get('/districts/residents/beneficiaries', response_model=list[schemas.BeneficiariesByDistrict], tags=['Sozialatlas'])
async def get_residents_beneficiaries_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_beneficiaries_by_districts(session)
    schema = schemas.BeneficiariesByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router1.get('/{district_id}/residents/beneficiaries', response_model=list[schemas.BeneficiariesByDistrict], tags=['Sozialatlas'])
async def get_residents_beneficiaries_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_beneficiaries_by_district(session, district_id)
    schema = schemas.BeneficiariesByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@router1.get('/districts/residents/beneficiaries/inactive', response_model=list[schemas.InactiveBeneficiariesInHouseholdsByDistrict], tags=['Sozialatlas'])
async def get_residents_beneficiaries_inactive_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_beneficiaries_inactive_by_districts(session)
    schema = schemas.InactiveBeneficiariesInHouseholdsByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router1.get('/{district_id}/residents/beneficiaries/inactive', response_model=list[schemas.InactiveBeneficiariesInHouseholdsByDistrict], tags=['Sozialatlas'])
async def get_residents_beneficiaries_inactive_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_beneficiaries_inactive_by_district(session, district_id)
    schema = schemas.InactiveBeneficiariesInHouseholdsByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@router1.get('/districts/residents/beneficiaries/characteristics', response_model=list[schemas.BeneficiariesCharacteristicsByDistrict], tags=['Sozialatlas'])
async def get_residents_beneficiaries_by_characteristics_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_beneficiaries_characteristics_by_districts(session)
    schema = schemas.BeneficiariesCharacteristicsByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        unemployability=r.unemployability,
        employability=r.employability,
        percentage_females=r.percentage_females,
        percentage_single_parents=r.percentage_single_parents,
        percentage_foreign_citizenship=r.percentage_foreign_citizenship) for r in rows]


@router1.get('/{district_id}/residents/beneficiaries/characteristics', response_model=list[schemas.BeneficiariesCharacteristicsByDistrict], tags=['Sozialatlas'])
async def get_residents_beneficiaries_by_characteristics_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_beneficiaries_characteristics_by_district(session, district_id)
    schema = schemas.BeneficiariesCharacteristicsByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        unemployability=r.unemployability,
        employability=r.employability,
        percentage_females=r.percentage_females,
        percentage_single_parents=r.percentage_single_parents,
        percentage_foreign_citizenship=r.percentage_foreign_citizenship) for r in rows]



@router1.get('/districts/residents/beneficiaries/age15tounder65', response_model=list[schemas.BeneficiariesAge15ToUnder65ByDistrict], tags=['Sozialatlas'])
async def get_residents_beneficiaries_age15tounder65_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_beneficiaries_age15tounder65_by_districts(session)
    schema = schemas.BeneficiariesAge15ToUnder65ByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        percentage_of_total_residents=r.percentage_of_total_residents,
        employable_with_benefits=r.employable_with_benefits,
        unemployment_benefits=r.unemployment_benefits,
        basic_income=r.basic_income,
        assisting_benefits=r.assisting_benefits) for r in rows]


@router1.get('/{district_id}/residents/beneficiaries/age15tounder65', response_model=list[schemas.BeneficiariesAge15ToUnder65ByDistrict], tags=['Sozialatlas'])
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



@router1.get('/districts/residents/migration/background', response_model=list[schemas.MigrationBackgroundByDistrict], tags=['Sozialatlas'])
async def get_residents_migration_background_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_migration_background_by_districts(session)
    schema = schemas.MigrationBackgroundByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        foreign_citizenship=r.foreign_citizenship,
        german_citizenship=r.german_citizenship) for r in rows]


@router1.get('/{district_id}/residents/migration/background', response_model=list[schemas.MigrationBackgroundByDistrict], tags=['Sozialatlas'])
async def get_residents_migration_background_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_migration_background_by_district(session, district_id)
    schema = schemas.MigrationBackgroundByDistrict

    return [schema(year=r.year,
        district_id=r.district_id,
        foreign_citizenship=r.foreign_citizenship,
        german_citizenship=r.german_citizenship) for r in rows]



@router1.get('/districts/residents/housing/assistance', response_model=list[schemas.HousingAssistanceCasesByDistrict], tags=['Sozialatlas'])
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


@router1.get('/{district_id}/residents/housing/assistance', response_model=list[schemas.HousingAssistanceCasesByDistrict], tags=['Sozialatlas'])
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



@router1.get('/districts/residents/housing/benefit', response_model=list[schemas.HousingBenefitByDistrict], tags=['Sozialatlas'])
async def get_residents_housing_benefit_by_district(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_housing_benefit_by_districts(session)
    schema = schemas.HousingBenefitByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@router1.get('/districts/residents/housing/benefit', response_model=list[schemas.HousingBenefitByDistrict], tags=['Sozialatlas'])
async def get_residents_housing_benefit_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_housing_benefit_by_districts(session)
    schema = schemas.HousingBenefitByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router1.get('/{district_id}/residents/housing/benefit', response_model=list[schemas.HousingBenefitByDistrict], tags=['Sozialatlas'])
async def get_residents_housing_benefit_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_housing_benefit_by_district(session, district_id)
    schema = schemas.HousingBenefitByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



@router1.get('/districts/residents/risk/homelessness',
        response_model=list[schemas.HouseholdsAtRiskOfHomelessnessByDistricts], tags=['Sozialatlas'])
async def get_residents_risk_homelessness_by_districts(session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_risk_homelessness_by_districts(session)
    schema = schemas.HouseholdsAtRiskOfHomelessnessByDistricts

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]


@router1.get('/{district_id}/residents/risk/homelessness', response_model=list[schemas.HouseholdsAtRiskOfHomelessnessByDistrict], tags=['Sozialatlas'])
async def get_residents_risk_homelessness_by_district(district_id: int, session: AsyncSession = Depends(get_session)):
    rows = await service.get_residents_risk_homelessness_by_district(session, district_id)
    schema = schemas.HouseholdsAtRiskOfHomelessnessByDistrict

    return [schema(year=r.year, district_id=r.district_id, residents=r.residents) for r in rows]



app.include_router(router6)
app.include_router(router5)
app.include_router(router4)
app.include_router(router1)
app.include_router(router2)
app.include_router(router3)
