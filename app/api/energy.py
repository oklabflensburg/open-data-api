from fastapi import Depends, APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..dependencies import get_session
from ..services.energy import *

route_energy = APIRouter(prefix='/energy/v1')


@route_energy.get(
    '/meta/state',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of German states with corresponding ids.')
)
async def fetch_energy_state_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_energy_state_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Could not retrieve list of German state codes')


@route_energy.get(
    '/meta/country',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of countries provided by the German market master data register.')
)
async def fetch_energy_country_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_energy_country_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Could not retrieve list of country codes')


@route_energy.get(
    '/meta/audit',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of network operator audit codes provided by the German market master data register')
)
async def fetch_network_operator_audit_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_network_operator_audit_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Could not retrieves list of network operator audit codes')


@route_energy.get(
    '/meta/location',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of energy location codes')
)
async def fetch_energy_location_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_energy_location_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Could not retrieve list of energy location codes')


@route_energy.get(
    '/meta/supply/type',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of energy supply types')
)
async def fetch_energy_supply_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_energy_supply_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Could not retrieves a list of energy supply types')


@route_energy.get(
    '/meta/source/type',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of energy source types')
)
async def fetch_energy_source_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_energy_source_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Could not retrieves list of energy source types')


@route_energy.get(
    '/meta/manufacturer',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of turbine manufacturers.')
)
async def fetch_turbine_manufacturer_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_turbine_manufacturer_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Turbine manufacturer not found')


@route_energy.get(
    '/meta/power/limitation',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of power limitations.')
)
async def fetch_power_limitation_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_power_limitation_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Power limitation not found')


@route_energy.get(
    '/meta/power/technology',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of power technologies.')
)
async def fetch_power_technology_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_power_technology_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Power technology not found')


@route_energy.get(
    '/meta/orientation',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of main orientations.')
)
async def fetch_main_orientation_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_main_orientation_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Main orientation not found')


@route_energy.get(
    '/meta/orientation/angle',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of orientation tilt angles.')
)
async def fetch_orientation_tilt_angle_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_orientation_tilt_angle_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Orientation tilt angle not found')


@route_energy.get(
    '/meta/usage/area',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of usage areas.')
)
async def fetch_usage_area_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_usage_area_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Usage area not found')


@route_energy.get(
    '/meta/operational/status',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of operational statuses.')
)
async def fetch_operational_status_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_operational_status_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Operational status not found')


@route_energy.get(
    '/meta/biomass/type',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of biomass types.')
)
async def fetch_biomass_type_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_biomass_type_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Biomass type not found')


@route_energy.get(
    '/meta/primary/fuel',
    response_model=List,
    tags=['Marktstammdatenregister Meta'],
    description=('Retrieves a list of primary fuels.')
)
async def fetch_primary_fuel_meta(
    session: AsyncSession = Depends(get_session)
):
    rows = await get_primary_fuel_meta(session)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response)
    except IndexError as e:
        raise HTTPException(status_code=404, detail='Primary fuel not found')



@route_energy.get(
    '/unit/combustion/id',
    response_model=List,
    tags=['Marktstammdatenregister Combustion'],
    description=('Retrieves details about a specific combustion unit based on the provided 15 digit unit registration number.')
)
async def fetch_combustion_unit_by_id(
    unit_id: str = Query(None, min_length=15, max_length=15),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_combustion_unit_by_id(session, unit_id)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'Combustion unit with id "{unit_id}" not found')


@route_energy.get(
    '/unit/combustion/key',
    response_model=List,
    tags=['Marktstammdatenregister Combustion'],
    description=('Retrieves a list of combustion units with each detail based on the provided German municipality key (AGS).')
)
async def fetch_combustion_unit_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_combustion_unit_by_municipality_key(session, municipality_key)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No combustion units for municipality key {municipality_key} found')

    return JSONResponse(content=response)



@route_energy.get(
    '/unit/nuclear/id',
    response_model=List,
    tags=['Marktstammdatenregister Nuclear'],
    description=('Retrieves details about a specific nuclear unit based on the provided 15 digit unit registration number.')
)
async def fetch_nuclear_unit_by_id(
    unit_id: str = Query(None, min_length=15, max_length=15),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_nuclear_unit_by_id(session, unit_id)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'Nuclear unit with id "{unit_id}" not found')


@route_energy.get(
    '/unit/nuclear/key',
    response_model=List,
    tags=['Marktstammdatenregister Nuclear'],
    description=('Retrieves a list of nuclear units with each detail based on the provided German municipality key (AGS).')
)
async def fetch_nuclear_unit_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_nuclear_unit_by_municipality_key(session, municipality_key)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No nuclear units for municipality key {municipality_key} found')

    return JSONResponse(content=response)



@route_energy.get(
    '/unit/water/id',
    response_model=List,
    tags=['Marktstammdatenregister Water'],
    description=('Retrieves details about a specific water unit based on the provided 15 digit unit registration number.')
)
async def fetch_water_unit_by_id(
    unit_id: str = Query(None, min_length=15, max_length=15),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_water_unit_by_id(session, unit_id)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'Water unit with id "{unit_id}" not found')


@route_energy.get(
    '/unit/water/key',
    response_model=List,
    tags=['Marktstammdatenregister Water'],
    description=('Retrieves a list of water units with each detail based on the provided German municipality key (AGS).')
)
async def fetch_water_unit_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_water_unit_by_municipality_key(session, municipality_key)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No water units for municipality key {municipality_key} found')

    return JSONResponse(content=response)



@route_energy.get(
    '/unit/biomass/id',
    response_model=List,
    tags=['Marktstammdatenregister Biomass'],
    description=('Retrieves details about a specific biomass unit based on the provided 15 digit unit registration number.')
)
async def fetch_biomass_unit_by_id(
    unit_id: str = Query(None, min_length=15, max_length=15),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_biomass_unit_by_id(session, unit_id)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'Biomass unit with id "{unit_id}" not found')


@route_energy.get(
    '/unit/biomass/key',
    response_model=List,
    tags=['Marktstammdatenregister Biomass'],
    description=('Retrieves a list of biomass units with each details based on the provided german municipality key (AGS).')
)
async def fetch_biomass_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_biomass_unit_by_municipality_key(session, municipality_key)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No biomass units for municipality key {municipality_key} found')

    return JSONResponse(content=response)



@route_energy.get(
    '/unit/wind/id',
    response_model=List,
    tags=['Marktstammdatenregister Wind'],
    description=('Retrieves details about a specific wind turbine unit based on the provided 15 digit unit registration number.')
)
async def fetch_wind_unit_by_id(
    unit_id: str = Query(None, min_length=15, max_length=15),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_wind_unit_by_id(session, unit_id)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'Wind turbine unit with id "{unit_id}" not found')


@route_energy.get(
    '/unit/wind/key',
    response_model=List,
    tags=['Marktstammdatenregister Wind'],
    description=('Retrieves a list of wind turbine units with each details based on the provided german municipality key (AGS).')
)
async def fetch_wind_unit_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_wind_unit_by_municipality_key(session, municipality_key)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No wind turbine units for municipality key {municipality_key} found')

    return JSONResponse(content=response)



@route_energy.get(
    '/unit/solar/id',
    response_model=List,
    tags=['Marktstammdatenregister Solar'],
    description=('Retrieves the solar unit details based on the provided 15 digit unit registration number.')
)
async def fetch_solar_unit_by_id(
    unit_id: str = Query(None, min_length=15, max_length=15),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_solar_unit_by_id(session, unit_id)
    response = jsonable_encoder(rows)

    try:
        return JSONResponse(content=response[0])
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f'Solar unit with id "{unit_id}" not found')


@route_energy.get(
    '/unit/solar/key',
    response_model=List,
    tags=['Marktstammdatenregister Solar'],
    description=('Retrieves a list of solar units with each details based on the provided german municipality key (AGS).')
)
async def fetch_solar_unit_by_municipality_key(
    municipality_key: str = Query(None, min_length=8, max_length=8),
    session: AsyncSession = Depends(get_session)
):
    rows = await get_solar_unit_by_municipality_key(session, municipality_key)
    response = jsonable_encoder(rows)

    if len(response) == 0:
        raise HTTPException(status_code=404, detail=f'No solar units for municipality key {municipality_key} found')

    return JSONResponse(content=response)
