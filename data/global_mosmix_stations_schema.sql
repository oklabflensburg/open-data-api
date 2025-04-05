-- TABELLE WETTERSTATIONEN MOSMIX
DROP TABLE IF EXISTS global_mosmix_stations CASCADE;

CREATE TABLE IF NOT EXISTS global_mosmix_stations (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR NOT NULL,
    icao_code VARCHAR,
    station_name VARCHAR,
    latitude NUMERIC(8, 6) NOT NULL,
    longitude NUMERIC(9, 6) NOT NULL,
    station_elevation INT,
    wkb_geometry GEOMETRY(POINT, 4326)
);

-- GEOMETRY INDEX
CREATE INDEX IF NOT EXISTS gis_global_mosmix_geometry ON global_mosmix_stations USING GIST (wkb_geometry);

-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_global_mosmix_station_id ON global_mosmix_stations (station_id);
