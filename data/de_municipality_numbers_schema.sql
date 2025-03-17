-- HILFSTABELLE AMTLICHE GEMEINDESCHLÜSSEL DEUTSCHLAND
DROP TABLE IF EXISTS de_municipality_numbers CASCADE;

CREATE TABLE IF NOT EXISTS de_municipality_numbers (
    id SERIAL PRIMARY KEY,
    municipality_number VARCHAR(8),
    municipality_name VARCHAR,
    notes VARCHAR
);


-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_municipality_number ON de_municipality_numbers (municipality_number);
