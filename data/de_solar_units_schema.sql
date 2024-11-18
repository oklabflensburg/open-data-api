-- TABELLE SOLAR EINHEITEN DEUTSCHLAND
DROP TABLE IF EXISTS de_solar_units CASCADE;

CREATE TABLE IF NOT EXISTS de_solar_units (
    id SERIAL PRIMARY KEY,
    unit_registration_number VARCHAR,
    last_update TIMESTAMP WITH TIME ZONE,
    location_registration_number VARCHAR,
    network_operator_audit_id INT,
    operator_registration_number VARCHAR,
    country_id INT,
    state_id INT,
    district VARCHAR,
    municipality_name VARCHAR,
    municipality_key VARCHAR,
    postcode VARCHAR,
    city VARCHAR,
    registration_date TIMESTAMP WITH TIME ZONE,
    commissioning_date TIMESTAMP WITH TIME ZONE,
    unit_system_status_id INT,
    unit_operational_status VARCHAR,
    not_present_migrated_units VARCHAR,
    power_unit_name VARCHAR,
    weic_not_available VARCHAR,
    power_plant_number_not_available VARCHAR,
    energy_source_id INT,
    gross_power NUMERIC,
    net_rated_power NUMERIC,
    remote_controllability NUMERIC,
    supply_type_id INT,
    assigned_active_power_inverter NUMERIC,
    amount_modules INT,
    location_id INT,
    power_limitation_id INT,
    uniform_orientation_tilt_angle_id INT,
    main_orientation_id INT,
    main_orientation_tilt_angle_id INT,
    usage_area_id INT,
    eeg_registration_number VARCHAR
);


-- INDEX
CREATE INDEX IF NOT EXISTS idx_unit_solar_municipality_key ON de_solar_units (municipality_key);

-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_unq_solar_unit_reg_num ON de_solar_units (unit_registration_number);
