-- TABELLE WIND EINHEITEN DEUTSCHLAND
DROP TABLE IF EXISTS de_wind_units CASCADE;

CREATE TABLE IF NOT EXISTS de_wind_units (
    id SERIAL PRIMARY KEY,
    unit_registration_number VARCHAR,
    last_update TIMESTAMP WITH TIME ZONE,
    location_registration_number VARCHAR,
    network_operator_audit INT,
    operator_registration_number VARCHAR,
    country INT,
    state INT,
    district VARCHAR,
    municipality_name VARCHAR,
    municipality_key VARCHAR,
    postcode VARCHAR,
    cadastral_district VARCHAR,
    field_parcel_numbers VARCHAR,
    street_not_found VARCHAR,
    house_number_not_available VARCHAR,
    house_number_not_found VARCHAR,
    city VARCHAR,
    longitude FLOAT,
    latitude FLOAT,
    registration_date TIMESTAMP WITH TIME ZONE,
    commissioning_date TIMESTAMP WITH TIME ZONE,
    unit_system_status VARCHAR,
    unit_operational_status VARCHAR,
    not_present_migrated_units VARCHAR,
    power_unit_name VARCHAR,
    weic_not_available VARCHAR,
    power_plant_number_not_available VARCHAR,
    energy_source VARCHAR,
    gross_power VARCHAR,
    net_rated_power VARCHAR,
    connection_high_voltage VARCHAR,
    remote_control_capability_nb VARCHAR,
    remote_control_capability_dv VARCHAR,
    supply_type VARCHAR,
    gen_registration_number VARCHAR,
    wind_park_name VARCHAR,
    location VARCHAR,
    manufacturer VARCHAR,
    technology VARCHAR,
    model_designation VARCHAR,
    hub_height VARCHAR,
    rotor_diameter VARCHAR,
    rotor_blade_deicing_system VARCHAR,
    shutdown_power_limitation VARCHAR,
    eeg_registration_number VARCHAR,
    wkb_geometry GEOMETRY(POINT, 4326)
);


-- INDEX
CREATE INDEX IF NOT EXISTS idx_wind_unit_municipality_key ON de_wind_units (municipality_key);

-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_unq_wind_unit_reg_num ON de_wind_units (unit_registration_number);

-- GEOMETRY INDEX
CREATE INDEX IF NOT EXISTS idx_wind_unit_geometry ON de_wind_units USING GIST (wkb_geometry);
