-- TABELLE KERNKRAFT EINHEITEN DEUTSCHLAND
DROP TABLE IF EXISTS de_nuclear_units CASCADE;

CREATE TABLE IF NOT EXISTS de_nuclear_units (
    id SERIAL PRIMARY KEY,
    unit_registration_number VARCHAR,
    last_update TIMESTAMP,
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
    house_number_not_available VARCHAR,
    house_number_not_found VARCHAR,
    location VARCHAR,
    longitude NUMERIC,
    latitude NUMERIC,
    registration_date TIMESTAMP,
    commissioning_date TIMESTAMP,
    decommissioning_date TIMESTAMP,
    unit_system_status_id INT,
    unit_operational_status_id INT,
    not_present_in_migrated_units VARCHAR,
    operator_change_date TIMESTAMP,
    operator_change_registration_date TIMESTAMP,
    unit_name VARCHAR,
    weic_not_available VARCHAR,
    plant_number_not_available VARCHAR,
    energy_source_id INT,
    gross_capacity NUMERIC,
    net_nominal_capacity NUMERIC,
    supply_type_id INT,
    plant_name VARCHAR,
    plant_block_name VARCHAR,
    technology_id INT,
    wkb_geometry GEOMETRY(POINT, 4326)
);


-- INDEX
CREATE INDEX IF NOT EXISTS idx_nuclear_unit_municipality_key ON de_nuclear_units (municipality_key);

-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_unq_nuclear_unit_reg_num ON de_nuclear_units (unit_registration_number);

-- GEOMETRY INDEX
CREATE INDEX IF NOT EXISTS idx_nuclear_unit_geometry ON de_nuclear_units USING GIST (wkb_geometry);
