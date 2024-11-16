-- TABELLE SOLAR EINHEITEN DEUTSCHLAND
DROP TABLE IF EXISTS de_solar_units CASCADE;

CREATE TABLE IF NOT EXISTS de_solar_units (
    id SERIAL PRIMARY KEY,
    unit_registration_number VARCHAR,
    last_update TIMESTAMP WITH TIME ZONE,
    location_registration_number VARCHAR,
    network_operator_audit INT,
    operator_registration_number VARCHAR,
    country VARCHAR,
    state VARCHAR,
    district VARCHAR,
    municipality_name VARCHAR,
    municipality_key VARCHAR,
    postcode VARCHAR,
    city VARCHAR,
    registration_date TIMESTAMP WITH TIME ZONE,
    commissioning_date TIMESTAMP WITH TIME ZONE,
    system_status VARCHAR,
    unit_operational_status VARCHAR,
    not_present_migrated_units VARCHAR,
    power_unit_name VARCHAR,
    weic_not_available VARCHAR,
    power_plant_number_not_available VARCHAR,
    energy_source VARCHAR,
    gross_power VARCHAR,
    net_rated_power VARCHAR,
    remote_controllability VARCHAR,
    supply_type VARCHAR,
    assigned_active_power_inverter VARCHAR,
    amount_modules VARCHAR,
    location VARCHAR,
    power_limitation VARCHAR,
    uniform_orientation_tilt_angle VARCHAR,
    main_orientation VARCHAR,
    main_orientation_tilt_angle VARCHAR,
    usage_area VARCHAR,
    eeg_registration_number VARCHAR
);


-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_unq_solar_unit_reg_num ON de_solar_units (unit_registration_number);
