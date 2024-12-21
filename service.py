from sqlalchemy.sql import func, text, bindparam
from sqlalchemy.types import JSON
from sqlalchemy.sql.expression import cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased

import json
import models


async def get_dwd_stations_by_municipality_key(session: AsyncSession, municipality_key: str):
    DwdStationReference = models.DwdStationReference
    Vg250Gem = models.Vg250Gem

    geojson = cast(func.ST_AsGeoJSON(DwdStationReference.wkb_geometry, 15), JSON).label('geojson')
    gem_alias = aliased(Vg250Gem)

    stmt = (
        select(
            DwdStationReference.station_name,
            DwdStationReference.station_id,
            DwdStationReference.identifier,
            DwdStationReference.station_code,
            DwdStationReference.station_elevation,
            DwdStationReference.river_basin_id,
            DwdStationReference.state_name,
            func.to_char(DwdStationReference.recording_start, 'DD.MM.YYYY').label('recording_start'),
            func.to_char(DwdStationReference.recording_end, 'DD.MM.YYYY').label('recording_end'),
            geojson,
        )
        .join(
            gem_alias,
            func.ST_Contains(
                func.ST_Transform(gem_alias.geom, 4326),
                DwdStationReference.wkb_geometry
            )
        )
        .where(
            gem_alias.ags == bindparam('municipality_key'),
            gem_alias.gf == 4,
            DwdStationReference.recording_end > func.current_date() - text("INTERVAL '1 week'")
        )
    )

    result = await session.execute(stmt, {'municipality_key': municipality_key})
    return result.mappings().all()


async def get_weather_service_stations(session: AsyncSession):
    model = models.WeatherStation

    geojson = cast(func.ST_AsGeoJSON(model.wkb_geometry, 15), JSON).label('geojson')

    query = select(
        model.station_id,
        func.to_char(model.start_date, 'DD.MM.YYYY').label('start_date'),
        func.to_char(model.end_date, 'DD.MM.YYYY').label('end_date'),
        model.station_elevation,
        model.station_name,
        model.state_name,
        model.submission,
        geojson
    )

    result = await session.execute(query)

    return result.mappings().all()



async def get_energy_source_meta(session: AsyncSession):
    model = models.EnergySourceMeta
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
    model = models.EnergyCountryMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_network_operator_audit_meta(session: AsyncSession):
    model = models.NetworkOperatorAuditMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_energy_location_meta(session: AsyncSession):
    model = models.EnergyLocationMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_energy_supply_meta(session: AsyncSession):
    model = models.EnergySupplyMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_turbine_manufacturer_meta(session: AsyncSession):
    model = models.TurbineManufacturerMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_power_limitation_meta(session: AsyncSession):
    model = models.PowerLimitationMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_power_technology_meta(session: AsyncSession):
    model = models.PowerTechnologyMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_main_orientation_meta(session: AsyncSession):
    model = models.MainOrientationMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_orientation_tilt_angle_meta(session: AsyncSession):
    model = models.OrientationTiltAngleMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_usage_area_meta(session: AsyncSession):
    model = models.UsageAreaMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_operational_status_meta(session: AsyncSession):
    model = models.OperationalStatusMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_biomass_type_meta(session: AsyncSession):
    model = models.BiomassTypeMeta
    result = await session.execute(select(model))
    return result.scalars().all()


async def get_primary_fuel_meta(session: AsyncSession):
    model = models.PrimaryFuelMeta
    result = await session.execute(select(model))
    return result.scalars().all()



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



async def get_biotope_origin(session: AsyncSession, code: str):
    stmt = text('''
    SELECT
        bo.description
    FROM
        sh_biotope_origin AS bo
    WHERE
        LOWER(bo.code) = :code
    ''')

    sql = stmt.bindparams(code=code.lower())
    result = await session.execute(sql)

    return result.mappings().all()



async def get_biotope_meta_by_lat_lng(session: AsyncSession, lat: float, lng: float):
    stmt = text('''
    SELECT
        bm.code,
        bm.designation,
        b.kartierdatum AS mapping_date,
        b.biotopbez AS description,
        b.wertbiotop AS valuable_biotope,
        b.herkunft AS mapping_origin,
        bo.description AS mapping_origin_description,
        bo.remark AS mapping_origin_remark,
        b.ortnr AS place_number,
        CASE
            WHEN b.btschutz_1 IS NOT NULL AND b.btschutz_2 IS NOT NULL THEN b.btschutz_1 || ', ' || b.btschutz_2
            WHEN b.btschutz_1 IS NOT NULL THEN b.btschutz_1
            WHEN b.btschutz_2 IS NOT NULL THEN b.btschutz_2
            ELSE NULL
        END AS protection_reason,
        b.lrt_typ_1 AS habitat_type_1,
        b.lrt_typ_2 AS habitat_type_2,
        ht1.label AS habitat_label_1,
        ht2.label AS habitat_label_2,
        b.gemeindename AS place_name,
        ST_Area(ST_Transform(b.wkb_geometry, 3587)) AS shape_area,
        ST_AsGeoJSON(b.wkb_geometry, 15)::jsonb AS geojson
    FROM
        sh_biotope AS b
    JOIN
        sh_biotope_key AS bm
        ON b.hauptcode = bm.code
    LEFT JOIN sh_biotope_origin AS bo
        ON b.herkunft = bo.code
    LEFT JOIN de_habitat_types AS ht1
        ON b.lrt_typ_1 = ht1.code
    LEFT JOIN de_habitat_types AS ht2
        ON b.lrt_typ_2 = ht2.code
    WHERE
        ST_Contains(b.wkb_geometry, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326))
    ''')

    sql = stmt.bindparams(lat=lat, lng=lng)
    result = await session.execute(sql)

    return result.mappings().all()


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



async def get_monument_by_object_id(session: AsyncSession, object_id: int):
    stmt = text('''
    WITH monument_reasons AS (
        SELECT
            mxr.monument_id,
            string_agg(mr.label, ', ') AS reason_labels
        FROM
            sh_monument_x_reason AS mxr
        JOIN
            sh_monument_reason AS mr
        ON
            mxr.reason_id = mr.id
        GROUP BY
            mxr.monument_id
    )
    SELECT
        m.object_id,
        m.street,
        m.housenumber,
        m.postcode,
        m.city,
        m.image_url,
        m.designation,
        m.description,
        m.monument_type,
        r.reason_labels AS monument_reason,
        ST_AsGeoJSON(m.wkb_geometry, 15)::jsonb AS geojson
    FROM
        sh_monuments AS m
    LEFT JOIN
        sh_monument_reasons AS r
    ON
        m.id = r.monument_id
    WHERE
        m.object_id = :q
    ''')

    sql = stmt.bindparams(q=object_id)
    result = await session.execute(sql)
    rows = result.mappings().all()

    return [dict(row) for row in rows]



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
        'geometry', ST_AsGeoJSON(ap.geom)::json,
        'properties', json_build_object(
            'ujahr', ap.ujahr, 'ustunde', ap.ustunde, 'uwochentag', ap.uwochentag,
            'umonat', ap.umonat, 'uland', ap.uland, 'uart', ap.uart, 'utyp1', ap.utyp1,
            'ukategorie', ap.ukategorie, 'ulichtverh', ap.ulichtverh, 'istrad', ap.istrad,
            'istpkw', ap.istpkw, 'istfuss', ap.istfuss, 'istgkfz', ap.istgkfz,
            'istkrad', ap.istkrad, 'istsonstig', ap.istsonstig)
        ) AS feature
        FROM vg250_gem AS vg

        JOIN de_accident_points AS ap
        ON ST_Within(ap.geom, vg.geom)

        WHERE LOWER(vg.gen) = :q
        AND vg.gf = 4
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
                'sum_districts_area', ROUND(SUM(CAST( ST_Area(ST_Transform(d.geom, 3587)) / 1000000 AS numeric)), 2)
            ) AS summary
        FROM
            fl_districts AS d
        LEFT JOIN
            fl_residents_by_districts AS rd
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
            fl_districts AS d
        LEFT JOIN
            fl_residents_by_districts AS rd
        ON d.id = rd.district_id
        LEFT JOIN
            fl_births_by_districts AS bd
        ON d.id = bd.district_id
        AND bd.year = rd.year
        LEFT JOIN
            fl_age_ratio_by_districts AS ard
        ON d.id = ard.district_id
        AND ard.year = rd.year
        LEFT JOIN
            fl_children_age_under_18_by_districts AS cad
        ON d.id = cad.district_id
        AND cad.year = rd.year
        LEFT JOIN
            fl_age_groups_of_residents_by_districts AS agrd
        ON d.id = agrd.district_id
        AND agrd.year = rd.year
        LEFT JOIN
            fl_residents_age_18_to_under_65_by_districts AS ra1865d
        ON d.id = ra1865d.district_id
        AND rd.year = ra1865d.year
        LEFT JOIN
            fl_residents_age_65_and_above_by_districts AS ra65ad
        ON d.id = ra65ad.district_id
        AND ra65ad.year = rd.year
        LEFT JOIN
            fl_migration_background_by_districts AS mbd
        ON d.id = mbd.district_id
        AND mbd.year = rd.year
        LEFT JOIN
            fl_employed_with_pension_insurance_by_districts AS epid
        ON d.id = epid.district_id
        AND rd.year = epid.year
        LEFT JOIN
            fl_unemployed_residents_by_districts AS ued
        ON d.id = ued.district_id
        AND rd.year = ued.year
        LEFT JOIN
            fl_unemployed_residents_by_districts_categorized AS uecd
        ON d.id = uecd.district_id
        AND rd.year = uecd.year
        LEFT JOIN
            fl_housing_benefit_by_districts AS hbd
        ON d.id = hbd.district_id
        AND rd.year = hbd.year
        LEFT JOIN
            fl_housing_assistance_cases_by_districts AS hacd
        ON d.id = hacd.district_id
        AND rd.year = hacd.year
        LEFT JOIN
            fl_households_at_risk_of_homelessness_by_districts AS hrhd
        ON d.id = hrhd.district_id
        AND rd.year = hrhd.year
        LEFT JOIN
            fl_beneficiaries_age_15_to_under_65_by_districts AS ba1565d
        ON d.id = ba1565d.district_id
        AND rd.year = ba1565d.year
        LEFT JOIN
            fl_beneficiaries_by_districts AS bfd
        ON d.id = bfd.district_id
        AND rd.year = bfd.year
        LEFT JOIN
            fl_beneficiaries_characteristics_by_districts AS bcd
        ON d.id = bcd.district_id
        AND rd.year = bcd.year
        LEFT JOIN
            fl_inactive_beneficiaries_in_households_by_districts AS iad
        ON d.id = iad.district_id
        AND rd.year = iad.year
        LEFT JOIN
            fl_basic_benefits_income_by_districts AS bbid
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
    model = models.AgeGroupsOfResidents
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_by_age_group(session: AsyncSession, age_group_id: int):
    model = models.AgeGroupsOfResidents
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



async def get_residents(session: AsyncSession):
    model = models.ResidentsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_by_district(session: AsyncSession, district_id: int):
    model = models.ResidentsByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_births(session: AsyncSession):
    model = models.BirthsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_births_by_district(session: AsyncSession, district_id: int):
    model = models.BirthsByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_employed(session: AsyncSession):
    model = models.EmployedWithPensionInsuranceByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_employed_by_district(session: AsyncSession, district_id: int):
    model = models.EmployedWithPensionInsuranceByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_ageratio(session: AsyncSession):
    model = models.AgeRatioByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_ageratio_by_district(session: AsyncSession, district_id: int):
    model = models.AgeRatioByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_basicbenefits(session: AsyncSession):
    model = models.BasicBenefitsIncomeByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_basicbenefits_by_district(session: AsyncSession, district_id: int):
    model = models.BasicBenefitsIncomeByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_ageunder18(session: AsyncSession):
    model = models.ChildrenAgeUnder18ByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_ageunder18_by_district(session: AsyncSession, district_id: int):
    model = models.ChildrenAgeUnder18ByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_age18tounder65(session: AsyncSession):
    model = models.ResidentsAge18ToUnder65ByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_age18tounder65_by_district(session: AsyncSession, district_id: int):
    model = models.ResidentsAge18ToUnder65ByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_age65andabove(session: AsyncSession):
    model = models.ResidentsAge65AndAboveByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_age65andabove_by_district(session: AsyncSession, district_id: int):
    model = models.ResidentsAge65AndAboveByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_agegroups(session: AsyncSession):
    model = models.AgeGroupsOfResidentsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_agegroups_by_district(session: AsyncSession, district_id: int):
    model = models.AgeGroupsOfResidentsByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_beneficiaries(session: AsyncSession):
    model = models.BeneficiariesByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()



async def get_residents_unemployed(session: AsyncSession):
    model = models.UnemployedResidentsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_unemployed_by_district(session: AsyncSession, district_id: int):
    model = models.UnemployedResidentsByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_unemployed_by_categories(session: AsyncSession):
    model = models.UnemployedCategorizedResidentsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_unemployed_by_categories_by_district(session: AsyncSession, district_id: int):
    model = models.UnemployedCategorizedResidentsByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_beneficiaries_inactive(session: AsyncSession):
    model = models.InactiveBeneficiariesInHouseholdsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_beneficiaries_by_district(session: AsyncSession, district_id: int):
    model = models.BeneficiariesByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_beneficiaries_characteristics(session: AsyncSession):
    model = models.BeneficiariesCharacteristicsByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_beneficiaries_inactive_by_district(session: AsyncSession, district_id: int):
    model = models.InactiveBeneficiariesInHouseholdsByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_beneficiaries_age15tounder65(session: AsyncSession):
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



async def get_residents_migration_background(session: AsyncSession):
    model = models.MigrationBackgroundByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_migration_background_by_district(session: AsyncSession, district_id: int):
    model = models.MigrationBackgroundByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_housing_assistance(session: AsyncSession):
    model = models.HousingAssistanceCasesByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_housing_assistance_by_district(session: AsyncSession, district_id: int):
    model = models.HousingAssistanceCasesByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_housing_benefit(session: AsyncSession):
    model = models.HousingBenefitByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_housing_benefit_by_district(session: AsyncSession, district_id: int):
    model = models.HousingBenefitByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()



async def get_residents_risk_homelessness(session: AsyncSession):
    model = models.HouseholdsRiskOfHomelessnessByDistrict
    result = await session.execute(select(model))

    return result.scalars().all()


async def get_residents_risk_homelessness_by_district(session: AsyncSession, district_id: int):
    model = models.HouseholdsRiskOfHomelessnessByDistrict
    result = await session.execute(select(model).filter(model.district_id==district_id))

    return result.scalars().all()
