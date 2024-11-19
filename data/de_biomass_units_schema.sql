-- TABELLE WIND EINHEITEN DEUTSCHLAND
DROP TABLE IF EXISTS de_biomass_units CASCADE;

CREATE TABLE IF NOT EXISTS de_biomass_units (
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
    street VARCHAR,
    street_not_found VARCHAR,
    house_number VARCHAR,
    house_number_not_available VARCHAR,
    house_number_not_found VARCHAR,
    location VARCHAR,
    longitude NUMERIC,
    latitude NUMERIC,
    registration_date TIMESTAMP WITH TIME ZONE,
    commissioning_date TIMESTAMP WITH TIME ZONE,
    unit_system_status_id INT,
    unit_operational_status_id INT,
    not_present_in_migrated_units VARCHAR,
    unit_name VARCHAR,
    weic_not_available VARCHAR,
    plant_number_not_available VARCHAR,
    energy_source_id INT,
    gross_capacity NUMERIC,
    net_nominal_capacity NUMERIC,
    remote_control_capability_nb VARCHAR,
    remote_control_capability_dv VARCHAR,
    supply_type_id INT,
    generator_registration_number VARCHAR,
    primary_fuel_id INT,
    biomass_type_id INT,
    technology_id INT,
    eeg_registration_number VARCHAR,
    kwk_registration_number VARCHAR,
    wkb_geometry GEOMETRY(POINT, 4326)
);


-- INDEX
CREATE INDEX IF NOT EXISTS idx_biomass_unit_municipality_key ON de_biomass_units (municipality_key);

-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_unq_biomass_unit_reg_num ON de_biomass_units (unit_registration_number);

-- GEOMETRY INDEX
CREATE INDEX IF NOT EXISTS idx_biomass_unit_geometry ON de_biomass_units USING GIST (wkb_geometry);
