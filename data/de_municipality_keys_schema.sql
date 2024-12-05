-- HILFSTABELLE AMTLICHE GEMEINDESCHLÜSSEL DEUTSCHLAND
DROP TABLE IF EXISTS de_municipality_keys CASCADE;

CREATE TABLE IF NOT EXISTS de_municipality_keys (
    id SERIAL PRIMARY KEY,
    municipality_key VARCHAR(8),
    municipality_name VARCHAR,
    notes VARCHAR
);


-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_municipality_key ON de_municipality_keys (municipality_key);
