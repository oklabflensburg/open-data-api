-- TABELLE WETTERSTATIONEN DEUTSCHLAND
DROP TABLE IF EXISTS de_weather_stations CASCADE;

CREATE TABLE IF NOT EXISTS de_weather_stations (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    station_elevation INT,
    latitude NUMERIC NOT NULL,
    longitude NUMERIC NOT NULL,
    station_name VARCHAR,
    state_name VARCHAR,
    submission VARCHAR,
    wkb_geometry GEOMETRY(POINT, 4326)
);


-- GEOMETRY INDEX
CREATE INDEX IF NOT EXISTS idx_gist_dwd_station_geometry ON de_weather_stations USING GIST (wkb_geometry);

-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_dwd_station_id ON de_weather_stations (station_id);
