-- TABELLE DWD STATIONSLEXIKON
DROP TABLE IF EXISTS dwd_station_reference CASCADE;

CREATE TABLE IF NOT EXISTS dwd_station_reference (
    id SERIAL PRIMARY KEY,

    -- Stationsname
    station_name VARCHAR NOT NULL,

    -- Stations_ID
    station_id VARCHAR NOT NULL,

    -- Kennung
    identifier VARCHAR NOT NULL,

    -- Stationskennung
    station_code VARCHAR NOT NULL,

    -- Breite
    station_latitude NUMERIC,

    -- Breite
    station_longitude NUMERIC,

    -- Stationshöhe
    station_elevation INT,

    -- Flussgebiet
    river_basin_id INT,

    -- Bundesland
    state_name VARCHAR NOT NULL,

    -- Beginn
    recording_start DATE,

    -- Ende
    recording_end DATE,

    -- Geometry
    wkb_geometry GEOMETRY(POINT, 4326),

    -- Data consistency check
    CHECK (recording_end >= recording_start)
);


-- GEOMETRY INDEX
CREATE INDEX IF NOT EXISTS idx_gist_dwd_station_reference_geometry ON dwd_station_reference USING GIST (wkb_geometry);

-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_dwd_station_code_id_identifier ON dwd_station_reference (station_id, station_code, identifier);
