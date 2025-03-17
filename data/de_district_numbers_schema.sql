-- HILFSTABELLE AMTLICHE KREISSCHLÜSSEL DEUTSCHLAND
DROP TABLE IF EXISTS de_district_numbers CASCADE;

CREATE TABLE IF NOT EXISTS de_district_numbers (
    id SERIAL PRIMARY KEY,
    district_number VARCHAR(5),
    district_name VARCHAR,
    notes VARCHAR
);


-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_district_number ON de_district_numbers (district_number);
