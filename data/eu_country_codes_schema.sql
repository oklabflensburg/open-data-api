-- TABELLE LÄNDERCODES EUROPA
DROP TABLE IF EXISTS eu_country_codes CASCADE;

CREATE TABLE eu_country_codes (
    id SERIAL PRIMARY KEY,
    numeric_code VARCHAR NOT NULL,
    iso_code VARCHAR(10) NOT NULL,
    iso_3166_alpha2 VARCHAR(2) NOT NULL,
    iso_3166_alpha3 VARCHAR(3) NOT NULL,
    iso_3166_numeric VARCHAR(3) NOT NULL,
    state_abbreviation VARCHAR NOT NULL,
    state_name VARCHAR NOT NULL
);


-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_eu_country_state_abbreviation ON eu_country_codes (state_abbreviation);
