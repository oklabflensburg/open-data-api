from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.energy import *



async def get_energy_source_meta(session: AsyncSession):
    model = EnergySourceMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_energy_state_meta(session: AsyncSession):
    stmt = text('''
    SELECT
        esm.id, esm.name, lan.sn_l AS state_id,
        CASE WHEN lan.geom IS NOT NULL THEN
            jsonb_build_object(
            'xmin', ST_XMin(lan.geom),
            'ymin', ST_YMin(lan.geom),
            'xmax', ST_XMax(lan.geom),
            'ymax', ST_YMax(lan.geom))
        ELSE NULL END AS bbox
    FROM de_energy_state_meta AS esm
    LEFT JOIN
        vg250_lan AS lan
    ON
        lan.gen = esm.name
    AND
        lan.gf = 4
    ORDER BY
        lan.sn_l
    ''')

    result = await session.execute(stmt)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_energy_country_meta(session: AsyncSession):
    model = EnergyCountryMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_network_operator_audit_meta(session: AsyncSession):
    model = NetworkOperatorAuditMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_energy_location_meta(session: AsyncSession):
    model = EnergyLocationMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_energy_supply_meta(session: AsyncSession):
    model = EnergySupplyMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_turbine_manufacturer_meta(session: AsyncSession):
    model = TurbineManufacturerMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_power_limitation_meta(session: AsyncSession):
    model = PowerLimitationMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_power_technology_meta(session: AsyncSession):
    model = PowerTechnologyMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_main_orientation_meta(session: AsyncSession):
    model = MainOrientationMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_orientation_tilt_angle_meta(session: AsyncSession):
    model = OrientationTiltAngleMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_usage_area_meta(session: AsyncSession):
    model = UsageAreaMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_operational_status_meta(session: AsyncSession):
    model = OperationalStatusMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_biomass_type_meta(session: AsyncSession):
    model = BiomassTypeMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_primary_fuel_meta(session: AsyncSession):
    model = PrimaryFuelMeta
    result = await session.execute(select(model))
    return result.scalars().all()



async def get_combustion_unit_by_municipality_key(session: AsyncSession, key: str):
    stmt = text('''
    SELECT
        cu.unit_registration_number,
        cu.last_update,
        cu.unit_name,
        cu.location_registration_number,
        noa.name AS network_operator_audit,
        cu.operator_registration_number,
        ecm.name AS country,
        usm.name AS state,
        cu.district,
        cu.municipality_name,
        cu.municipality_key,
        cu.postcode,
        cu.street,
        cu.street_not_found,
        cu.house_number,
        cu.house_number_not_available,
        cu.house_number_not_found,
        cu.location,
        cu.registration_date,
        cu.commissioning_date,
        cu.unit_system_status_id,
        osm.name AS unit_operational_status,
        cu.not_present_in_migrated_units,
        cu.weic_not_available,
        cu.plant_number_not_available,
        esm.name AS energy_source,
        cu.gross_capacity,
        cu.net_nominal_capacity,
        cu.remote_control_nb,
        ust.name AS supply_type,
        cu.plant_name,
        cu.plant_block_name,
        pfm.name AS primary_fuel,
        cu.emergency_power_generator,
        cu.kwk_registration_number,
        ptu.name AS technology,
        ST_AsGeoJSON(cu.wkb_geometry, 15)::jsonb AS geojson
    FROM
        de_combustion_units AS cu
    LEFT JOIN
        de_energy_country_meta AS ecm ON ecm.id = cu.country_id
    LEFT JOIN
        de_energy_source_meta AS esm ON esm.id = cu.energy_source_id
    LEFT JOIN
        de_energy_state_meta AS usm ON usm.id = cu.state_id
    LEFT JOIN
        de_energy_supply_meta AS ust ON ust.id = cu.supply_type_id
    LEFT JOIN
        de_network_operator_audit_meta AS noa ON noa.id = cu.network_operator_audit_id
    LEFT JOIN
        de_operational_status_meta AS osm ON osm.id = cu.unit_operational_status_id
    LEFT JOIN
        de_power_technology_meta AS ptu ON ptu.id = cu.technology_id
    LEFT JOIN
        de_primary_fuel_meta AS pfm ON pfm.id = cu.primary_fuel_id
    WHERE
        LOWER(municipality_key) = :key
    ''')

    sql = stmt.bindparams(key=key.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_combustion_unit_by_id(session: AsyncSession, unit_id: str):
    stmt = text('''
    SELECT
        cu.unit_registration_number,
        cu.last_update,
        cu.unit_name,
        cu.location_registration_number,
        noa.name AS network_operator_audit,
        cu.operator_registration_number,
        ecm.name AS country,
        usm.name AS state,
        cu.district,
        cu.municipality_name,
        cu.municipality_key,
        cu.postcode,
        cu.street,
        cu.street_not_found,
        cu.house_number,
        cu.house_number_not_available,
        cu.house_number_not_found,
        cu.location,
        cu.registration_date,
        cu.commissioning_date,
        cu.unit_system_status_id,
        osm.name AS unit_operational_status,
        cu.not_present_in_migrated_units,
        cu.weic_not_available,
        cu.plant_number_not_available,
        esm.name AS energy_source,
        cu.gross_capacity,
        cu.net_nominal_capacity,
        cu.remote_control_nb,
        ust.name AS supply_type,
        cu.plant_name,
        cu.plant_block_name,
        pfm.name AS primary_fuel,
        cu.emergency_power_generator,
        cu.kwk_registration_number,
        ptu.name AS technology,
        ST_AsGeoJSON(cu.wkb_geometry, 15)::jsonb AS geojson
    FROM
        de_combustion_units AS cu
    LEFT JOIN
        de_energy_country_meta AS ecm ON ecm.id = cu.country_id
    LEFT JOIN
        de_energy_source_meta AS esm ON esm.id = cu.energy_source_id
    LEFT JOIN
        de_energy_state_meta AS usm ON usm.id = cu.state_id
    LEFT JOIN
        de_energy_supply_meta AS ust ON ust.id = cu.supply_type_id
    LEFT JOIN
        de_network_operator_audit_meta AS noa ON noa.id = cu.network_operator_audit_id
    LEFT JOIN
        de_operational_status_meta AS osm ON osm.id = cu.unit_operational_status_id
    LEFT JOIN
        de_power_technology_meta AS ptu ON ptu.id = cu.technology_id
    LEFT JOIN
        de_primary_fuel_meta AS pfm ON pfm.id = cu.primary_fuel_id
    WHERE
        LOWER(unit_registration_number) = :unit_id
    ''')

    sql = stmt.bindparams(unit_id=unit_id.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]



async def get_nuclear_unit_by_municipality_key(session: AsyncSession, key: str):
    stmt = text('''
    SELECT
        unit_registration_number,
        last_update,
        unit_name,
        location_registration_number,
        noa.name AS network_operator_audit,
        operator_registration_number,
        ecm.name AS country,
        usm.name AS state,
        district,
        municipality_name,
        municipality_key,
        postcode,
        street,
        street_not_found,
        house_number_not_available,
        house_number_not_found,
        location,
        registration_date,
        commissioning_date,
        decommissioning_date,
        unit_system_status_id,
        osm.name AS unit_operational_status,
        not_present_in_migrated_units,
        operator_change_date,
        operator_change_registration_date,
        weic_not_available,
        plant_number_not_available,
        esm.name AS energy_source,
        gross_capacity,
        net_nominal_capacity,
        ust.name AS supply_type,
        plant_name,
        plant_block_name,
        ptu.name AS technology,
        ST_AsGeoJSON(wkb_geometry, 15)::jsonb AS geojson
    FROM
        de_nuclear_units AS nu
    LEFT JOIN
        de_energy_country_meta AS ecm ON ecm.id = nu.country_id
    LEFT JOIN
        de_energy_source_meta AS esm ON esm.id = nu.energy_source_id
    LEFT JOIN
        de_energy_state_meta AS usm ON usm.id = nu.state_id
    LEFT JOIN
        de_energy_supply_meta AS ust ON ust.id = nu.supply_type_id
    LEFT JOIN
        de_network_operator_audit_meta AS noa ON noa.id = nu.network_operator_audit_id
    LEFT JOIN
        de_operational_status_meta AS osm ON osm.id = nu.unit_operational_status_id
    LEFT JOIN
        de_power_technology_meta AS ptu ON ptu.id = nu.technology_id
    WHERE
        LOWER(municipality_key) = :key
    ''')

    sql = stmt.bindparams(key=key.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_nuclear_unit_by_id(session: AsyncSession, unit_id: str):
    stmt = text('''
    SELECT
        unit_registration_number,
        last_update,
        unit_name,
        location_registration_number,
        noa.name AS network_operator_audit,
        operator_registration_number,
        ecm.name AS country,
        usm.name AS state,
        district,
        municipality_name,
        municipality_key,
        postcode,
        street,
        street_not_found,
        house_number_not_available,
        house_number_not_found,
        location,
        registration_date,
        commissioning_date,
        decommissioning_date,
        unit_system_status_id,
        osm.name AS unit_operational_status,
        not_present_in_migrated_units,
        operator_change_date,
        operator_change_registration_date,
        weic_not_available,
        plant_number_not_available,
        esm.name AS energy_source,
        gross_capacity,
        net_nominal_capacity,
        ust.name AS supply_type,
        plant_name,
        plant_block_name,
        ptu.name AS technology,
        ST_AsGeoJSON(wkb_geometry, 15)::jsonb AS geojson
    FROM
        de_nuclear_units AS nu
    LEFT JOIN
        de_energy_country_meta AS ecm ON ecm.id = nu.country_id
    LEFT JOIN
        de_energy_source_meta AS esm ON esm.id = nu.energy_source_id
    LEFT JOIN
        de_energy_state_meta AS usm ON usm.id = nu.state_id
    LEFT JOIN
        de_energy_supply_meta AS ust ON ust.id = nu.supply_type_id
    LEFT JOIN
        de_network_operator_audit_meta AS noa ON noa.id = nu.network_operator_audit_id
    LEFT JOIN
        de_operational_status_meta AS osm ON osm.id = nu.unit_operational_status_id
    LEFT JOIN
        de_power_technology_meta AS ptu ON ptu.id = nu.technology_id
    WHERE
        LOWER(unit_registration_number) = :unit_id
    ''')

    sql = stmt.bindparams(unit_id=unit_id.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]



async def get_water_unit_by_municipality_key(session: AsyncSession, key: str):
    stmt = text('''
    SELECT
        unit_registration_number,
        last_update,
        unit_name,
        location_registration_number,
        noa.name AS network_operator_audit,
        operator_registration_number,
        ecm.name AS country,
        usm.name AS state,
        district,
        municipality_name,
        municipality_key,
        postcode,
        cadastral_district,
        field_parcel_numbers,
        street_not_found,
        house_number_not_available,
        house_number_not_found,
        location,
        registration_date,
        commissioning_date,
        unit_system_status_id,
        osm.name AS unit_operational_status,
        inflow_type_id,
        not_present_in_migrated_units,
        operator_change_date,
        operator_change_registration_date,
        weic_not_available,
        plant_number_not_available,
        esm.name AS energy_source,
        gross_capacity,
        net_nominal_capacity,
        remote_control_capability_nb,
        ust.name AS supply_type,
        plant_name,
        hydropower_plant_type_id,
        power_generation_reduction,
        eeg_registration_number,
        ST_AsGeoJSON(wkb_geometry, 15)::jsonb AS geojson
    FROM
        de_water_units AS wu
    LEFT JOIN
        de_energy_country_meta AS ecm ON ecm.id = wu.country_id
    LEFT JOIN
        de_energy_source_meta AS esm ON esm.id = wu.energy_source_id
    LEFT JOIN
        de_energy_state_meta AS usm ON usm.id = wu.state_id
    LEFT JOIN
        de_energy_supply_meta AS ust ON ust.id = wu.supply_type_id
    LEFT JOIN
        de_network_operator_audit_meta AS noa ON noa.id = wu.network_operator_audit_id
    LEFT JOIN
        de_operational_status_meta AS osm ON osm.id = wu.unit_operational_status_id
    WHERE
        LOWER(municipality_key) = :key
    ''')

    sql = stmt.bindparams(key=key.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]



async def get_water_unit_by_id(session: AsyncSession, unit_id: str):
    stmt = text('''
    SELECT
        unit_registration_number,
        last_update,
        unit_name,
        location_registration_number,
        noa.name AS network_operator_audit,
        operator_registration_number,
        ecm.name AS country,
        usm.name AS state,
        district,
        municipality_name,
        municipality_key,
        postcode,
        cadastral_district,
        field_parcel_numbers,
        street_not_found,
        house_number_not_available,
        house_number_not_found,
        location,
        registration_date,
        commissioning_date,
        unit_system_status_id,
        osm.name AS unit_operational_status,
        inflow_type_id,
        not_present_in_migrated_units,
        operator_change_date,
        operator_change_registration_date,
        weic_not_available,
        plant_number_not_available,
        esm.name AS energy_source,
        gross_capacity,
        net_nominal_capacity,
        remote_control_capability_nb,
        ust.name AS supply_type,
        plant_name,
        hydropower_plant_type_id,
        power_generation_reduction,
        eeg_registration_number,
        ST_AsGeoJSON(wkb_geometry, 15)::jsonb AS geojson
    FROM
        de_water_units AS wu
    LEFT JOIN
        de_energy_country_meta AS ecm ON ecm.id = wu.country_id
    LEFT JOIN
        de_energy_source_meta AS esm ON esm.id = wu.energy_source_id
    LEFT JOIN
        de_energy_state_meta AS usm ON usm.id = wu.state_id
    LEFT JOIN
        de_energy_supply_meta AS ust ON ust.id = wu.supply_type_id
    LEFT JOIN
        de_network_operator_audit_meta AS noa ON noa.id = wu.network_operator_audit_id
    LEFT JOIN
        de_operational_status_meta AS osm ON osm.id = wu.unit_operational_status_id
    WHERE
        LOWER(unit_registration_number) = :unit_id
    ''')

    sql = stmt.bindparams(unit_id=unit_id.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]



async def get_biomass_unit_by_municipality_key(session: AsyncSession, key: str):
    stmt = text('''
    SELECT
        bu.unit_registration_number,
        bu.last_update,
        bu.unit_name,
        bu.location_registration_number,
        noa.name AS network_operator_audit,
        bu.operator_registration_number,
        ecm.name AS country,
        usm.name AS state,
        bu.district,
        bu.municipality_name,
        bu.municipality_key,
        bu.postcode,
        bu.street,
        bu.house_number,
        bu.street_not_found,
        bu.location,
        bu.house_number_not_available,
        bu.house_number_not_found,
        bu.registration_date,
        bu.commissioning_date,
        bu.unit_system_status_id,
        osm.name AS unit_operational_status,
        bu.not_present_in_migrated_units,
        bu.weic_not_available,
        bu.plant_number_not_available,
        esm.name AS energy_source,
        ust.name AS supply_type,
        bu.gross_capacity,
        ptu.name AS technology,
        bu.net_nominal_capacity,
        bu.remote_control_capability_nb,
        bu.remote_control_capability_dv,
        bu.generator_registration_number,
        pfm.name AS primary_fuel,
        btm.name AS biomass_type,
        bu.eeg_registration_number,
        bu.kwk_registration_number,
        ST_AsGeoJSON(bu.wkb_geometry)::jsonb AS geojson
    FROM
        de_biomass_units AS bu
    LEFT JOIN
        de_energy_country_meta AS ecm ON ecm.id = bu.country_id
    LEFT JOIN
        de_energy_source_meta AS esm ON esm.id = bu.energy_source_id
    LEFT JOIN
        de_energy_state_meta AS usm ON usm.id = bu.state_id
    LEFT JOIN
        de_energy_supply_meta AS ust ON ust.id = bu.supply_type_id
    LEFT JOIN
        de_network_operator_audit_meta AS noa ON noa.id = bu.network_operator_audit_id
    LEFT JOIN
        de_power_technology_meta AS ptu ON ptu.id = bu.technology_id
    LEFT JOIN
        de_operational_status_meta AS osm ON osm.id = bu.unit_operational_status_id
    LEFT JOIN
        de_biomass_type_meta AS btm ON btm.id = bu.biomass_type_id
    LEFT JOIN
        de_primary_fuel_meta AS pfm ON pfm.id = bu.primary_fuel_id
    WHERE
        LOWER(bu.municipality_key) = :key
    ''')

    sql = stmt.bindparams(key=key.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_biomass_unit_by_id(session: AsyncSession, unit_id: str):
    stmt = text('''
    SELECT
        bu.unit_registration_number,
        bu.last_update,
        bu.unit_name,
        bu.location_registration_number,
        noa.name AS network_operator_audit,
        bu.operator_registration_number,
        ecm.name AS country,
        usm.name AS state,
        bu.district,
        bu.municipality_name,
        bu.municipality_key,
        bu.postcode,
        bu.street,
        bu.house_number,
        bu.street_not_found,
        bu.location,
        bu.house_number_not_available,
        bu.house_number_not_found,
        bu.registration_date,
        bu.commissioning_date,
        bu.unit_system_status_id,
        osm.name AS unit_operational_status,
        bu.not_present_in_migrated_units,
        bu.weic_not_available,
        bu.plant_number_not_available,
        esm.name AS energy_source,
        ust.name AS supply_type,
        bu.gross_capacity,
        ptu.name AS technology,
        bu.net_nominal_capacity,
        bu.remote_control_capability_nb,
        bu.remote_control_capability_dv,
        bu.generator_registration_number,
        pfm.name AS primary_fuel,
        btm.name AS biomass_type,
        bu.eeg_registration_number,
        bu.kwk_registration_number,
        ST_AsGeoJSON(bu.wkb_geometry)::jsonb AS geojson
    FROM
        de_biomass_units AS bu
    LEFT JOIN
        de_energy_country_meta AS ecm ON ecm.id = bu.country_id
    LEFT JOIN
        de_energy_source_meta AS esm ON esm.id = bu.energy_source_id
    LEFT JOIN
        de_energy_state_meta AS usm ON usm.id = bu.state_id
    LEFT JOIN
        de_energy_supply_meta AS ust ON ust.id = bu.supply_type_id
    LEFT JOIN
        de_network_operator_audit_meta AS noa ON noa.id = bu.network_operator_audit_id
    LEFT JOIN
        de_power_technology_meta AS ptu ON ptu.id = bu.technology_id
    LEFT JOIN
        de_operational_status_meta AS osm ON osm.id = bu.unit_operational_status_id
    LEFT JOIN
        de_biomass_type_meta AS btm ON btm.id = bu.biomass_type_id
    LEFT JOIN
        de_primary_fuel_meta AS pfm ON pfm.id = bu.primary_fuel_id
    WHERE
        LOWER(unit_registration_number) = :unit_id
    ''')

    sql = stmt.bindparams(unit_id=unit_id.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]



async def get_wind_unit_by_municipality_key(session: AsyncSession, key: str):
    stmt = text('''
    SELECT
        wu.unit_registration_number,
        wu.last_update,
        wu.unit_name,
        wu.location_registration_number,
        noa.name AS network_operator_audit,
        wu.operator_registration_number,
        ecm.name AS country,
        usm.name AS state,
        wu.district,
        wu.city,
        elm.name AS location,
        wu.postcode,
        wu.municipality_name,
        wu.municipality_key,
        wu.cadastral_district,
        wu.field_parcel_numbers,
        wu.street_not_found,
        wu.house_number_not_available,
        wu.house_number_not_found,
        wu.registration_date,
        wu.commissioning_date,
        wu.unit_system_status_id,
        ust.name AS supply_type,
        osm.name AS unit_operational_status,
        wu.not_present_migrated_units,
        wu.weic_not_available,
        esm.name AS energy_source,
        wu.power_plant_number_not_available,
        wu.gross_capacity,
        wu.net_nominal_capacity,
        wu.connection_high_voltage,
        wu.remote_control_capability_nb,
        wu.remote_control_capability_dv,
        wu.gen_registration_number,
        wu.wind_park_name,
        wtm.name AS manufacturer,
        ptu.name AS technology,
        wu.model_designation,
        wu.hub_height,
        wu.rotor_diameter,
        wu.rotor_blade_deicing_system,
        wu.shutdown_power_limitation,
        wu.eeg_registration_number,
        ST_AsGeoJSON(wu.wkb_geometry)::jsonb AS geojson
    FROM
        de_wind_units AS wu
    LEFT JOIN
        de_energy_country_meta AS ecm ON ecm.id = wu.country_id
    LEFT JOIN
        de_energy_location_meta AS elm ON elm.id = wu.location_id
    LEFT JOIN
        de_energy_source_meta AS esm ON esm.id = wu.energy_source_id
    LEFT JOIN
        de_energy_state_meta AS usm ON usm.id = wu.state_id
    LEFT JOIN
        de_energy_supply_meta AS ust ON ust.id = wu.supply_type_id
    LEFT JOIN
        de_network_operator_audit_meta AS noa ON noa.id = wu.network_operator_audit_id
    LEFT JOIN
        de_power_technology_meta AS ptu ON ptu.id = wu.technology_id
    LEFT JOIN
        de_turbine_manufacturer_meta AS wtm ON wtm.id = wu.manufacturer_id
    LEFT JOIN
        de_operational_status_meta AS osm ON osm.id = wu.unit_operational_status_id
    WHERE
        LOWER(wu.municipality_key) = :key
    ''')

    sql = stmt.bindparams(key=key.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_wind_unit_by_id(session: AsyncSession, unit_id: str):
    stmt = text('''
    SELECT
        wu.unit_registration_number,
        wu.last_update,
        wu.unit_name,
        wu.location_registration_number,
        noa.name AS network_operator_audit,
        wu.operator_registration_number,
        ecm.name AS country,
        usm.name AS state,
        wu.district,
        wu.city,
        elm.name AS location,
        wu.postcode,
        wu.municipality_name,
        wu.municipality_key,
        wu.cadastral_district,
        wu.field_parcel_numbers,
        wu.street_not_found,
        wu.house_number_not_available,
        wu.house_number_not_found,
        wu.registration_date,
        wu.commissioning_date,
        wu.unit_system_status_id,
        ust.name AS supply_type,
        osm.name AS unit_operational_status,
        wu.not_present_migrated_units,
        wu.weic_not_available,
        esm.name AS energy_source,
        wu.power_plant_number_not_available,
        wu.gross_capacity,
        wu.net_nominal_capacity,
        wu.connection_high_voltage,
        wu.remote_control_capability_nb,
        wu.remote_control_capability_dv,
        wu.gen_registration_number,
        wu.wind_park_name,
        wtm.name AS manufacturer,
        ptu.name AS technology,
        wu.model_designation,
        wu.hub_height,
        wu.rotor_diameter,
        wu.rotor_blade_deicing_system,
        wu.shutdown_power_limitation,
        wu.eeg_registration_number,
        ST_AsGeoJSON(wu.wkb_geometry)::jsonb AS geojson
    FROM
        de_wind_units AS wu
    LEFT JOIN
        de_energy_country_meta AS ecm ON ecm.id = wu.country_id
    LEFT JOIN
        de_energy_location_meta AS elm ON elm.id = wu.location_id
    LEFT JOIN
        de_energy_source_meta AS esm ON esm.id = wu.energy_source_id
    LEFT JOIN
        de_energy_state_meta AS usm ON usm.id = wu.state_id
    LEFT JOIN
        de_energy_supply_meta AS ust ON ust.id = wu.supply_type_id
    LEFT JOIN
        de_network_operator_audit_meta AS noa ON noa.id = wu.network_operator_audit_id
    LEFT JOIN
        de_power_technology_meta AS ptu ON ptu.id = wu.technology_id
    LEFT JOIN
        de_turbine_manufacturer_meta AS wtm ON wtm.id = wu.manufacturer_id
    LEFT JOIN
        de_operational_status_meta AS osm ON osm.id = wu.unit_operational_status_id
    WHERE
        LOWER(unit_registration_number) = :unit_id
    ''')

    sql = stmt.bindparams(unit_id=unit_id.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]



async def get_solar_unit_by_municipality_key(session: AsyncSession, key: str):
    stmt = text('''
    SELECT
        su.unit_registration_number,
        su.last_update,
        su.location_registration_number,
        su.operator_registration_number,
        su.district,
        su.municipality_name,
        su.municipality_key,
        su.postcode,
        su.city,
        su.citizen_energy,
        su.network_operator_inspection_date,
        su.final_decommissioning_date,
        su.temporary_decommissioning_date,
        su.operation_resumption_date,
        su.planned_commissioning_date,
        su.legacy_system_registration_number,
        su.former_operator_registration_number,
        su.actual_operator_change_date,
        su.operator_change_registration_date,
        su.w_code,
        su.w_code_display_name,
        su.power_plant_number,
        su.high_voltage_connection,
        su.remote_control_direct_marketer,
        su.cadastral_district,
        su.plots_or_parcel_numbers,
        su.street,
        su.street_not_found,
        su.housenumber,
        su.housenumber_not_found,
        su.address_addition,
        su.longitude,
        su.latitude,
        su.utm_zone,
        su.utm_east,
        su.utm_north,
        su.gauss_kruger_north,
        su.gauss_kruger_east,
        su.black_start_capability,
        su.island_operation_capability,
        su.responsible_partner_number,
        su.registration_date,
        su.commissioning_date,
        su.not_present_migrated_units,
        su.unit_name,
        su.weic_not_available,
        su.power_plant_number_not_available,
        su.gross_capacity,
        su.net_nominal_capacity,
        su.remote_controllability,
        su.assigned_active_power_inverter,
        su.amount_modules,
        su.uniform_orientation_tilt_angle,
        su.eeg_registration_number,
        noa.name AS network_operator_audit,
        ecm.name AS country,
        usm.name AS state,
        elm.name AS location,
        osm.name AS unit_operational_status,
        uam.name AS usage_area,
        esm.name AS energy_source,
        ust.name AS supply_type,
        plm.name AS power_limitation,
        smo.name AS main_orientation,
        ota.name AS main_orientation_tilt_angle,
        ST_AsGeoJSON(su.wkb_geometry, 15)::jsonb AS geojson
    FROM
        de_solar_units AS su
    LEFT JOIN
        de_energy_country_meta AS ecm ON ecm.id = su.country_id
    LEFT JOIN
        de_energy_location_meta AS elm ON elm.id = su.location_id
    LEFT JOIN
        de_energy_source_meta AS esm ON esm.id = su.energy_source_id
    LEFT JOIN
        de_energy_state_meta AS usm ON usm.id = su.state_id
    LEFT JOIN
        de_energy_supply_meta AS ust ON ust.id = su.supply_type_id
    LEFT JOIN
        de_network_operator_audit_meta AS noa ON noa.id = su.network_operator_audit_id
    LEFT JOIN
        de_main_orientation_meta AS smo ON smo.id = su.main_orientation_id
    LEFT JOIN
        de_orientation_tilt_angle_meta AS ota ON ota.id = su.main_orientation_tilt_angle_id
    LEFT JOIN
        de_usage_area_meta AS uam ON uam.id = su.usage_area_id
    LEFT JOIN
        de_power_limitation_meta AS plm ON plm.id = su.power_limitation_id
    LEFT JOIN
        de_operational_status_meta AS osm ON osm.id = su.unit_operational_status_id
    WHERE
        LOWER(su.municipality_key) = :key
    ''')

    sql = stmt.bindparams(key=key.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]


async def get_solar_unit_by_id(session: AsyncSession, unit_id: str):
    stmt = text('''
    SELECT
        su.unit_registration_number,
        su.last_update,
        su.location_registration_number,
        su.operator_registration_number,
        su.district,
        su.municipality_name,
        su.municipality_key,
        su.postcode,
        su.city,
        su.citizen_energy,
        su.network_operator_inspection_date,
        su.final_decommissioning_date,
        su.temporary_decommissioning_date,
        su.operation_resumption_date,
        su.planned_commissioning_date,
        su.legacy_system_registration_number,
        su.former_operator_registration_number,
        su.actual_operator_change_date,
        su.operator_change_registration_date,
        su.w_code,
        su.w_code_display_name,
        su.power_plant_number,
        su.high_voltage_connection,
        su.remote_control_direct_marketer,
        su.cadastral_district,
        su.plots_or_parcel_numbers,
        su.street,
        su.street_not_found,
        su.housenumber,
        su.housenumber_not_found,
        su.address_addition,
        su.longitude,
        su.latitude,
        su.utm_zone,
        su.utm_east,
        su.utm_north,
        su.gauss_kruger_north,
        su.gauss_kruger_east,
        su.black_start_capability,
        su.island_operation_capability,
        su.responsible_partner_number,
        su.registration_date,
        su.commissioning_date,
        su.not_present_migrated_units,
        su.unit_name,
        su.weic_not_available,
        su.power_plant_number_not_available,
        su.gross_capacity,
        su.net_nominal_capacity,
        su.remote_controllability,
        su.assigned_active_power_inverter,
        su.amount_modules,
        su.uniform_orientation_tilt_angle,
        su.eeg_registration_number,
        noa.name AS network_operator_audit,
        ecm.name AS country,
        usm.name AS state,
        elm.name AS location,
        osm.name AS unit_operational_status,
        uam.name AS usage_area,
        esm.name AS energy_source,
        ust.name AS supply_type,
        plm.name AS power_limitation,
        smo.name AS main_orientation,
        ota.name AS main_orientation_tilt_angle,
        ST_AsGeoJSON(su.wkb_geometry, 15)::jsonb AS geojson
    FROM
        de_solar_units AS su
    LEFT JOIN
        de_energy_country_meta AS ecm ON ecm.id = su.country_id
    LEFT JOIN
        de_energy_location_meta AS elm ON elm.id = su.location_id
    LEFT JOIN
        de_energy_source_meta AS esm ON esm.id = su.energy_source_id
    LEFT JOIN
        de_energy_state_meta AS usm ON usm.id = su.state_id
    LEFT JOIN
        de_energy_supply_meta AS ust ON ust.id = su.supply_type_id
    LEFT JOIN
        de_network_operator_audit_meta AS noa ON noa.id = su.network_operator_audit_id
    LEFT JOIN
        de_main_orientation_meta AS smo ON smo.id = su.main_orientation_id
    LEFT JOIN
        de_orientation_tilt_angle_meta AS ota ON ota.id = su.main_orientation_tilt_angle_id
    LEFT JOIN
        de_usage_area_meta AS uam ON uam.id = su.usage_area_id
    LEFT JOIN
        de_power_limitation_meta AS plm ON plm.id = su.power_limitation_id
    LEFT JOIN
        de_operational_status_meta AS osm ON osm.id = su.unit_operational_status_id
    WHERE
        LOWER(unit_registration_number) = :unit_id
    ''')

    sql = stmt.bindparams(unit_id=unit_id.lower())
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]
