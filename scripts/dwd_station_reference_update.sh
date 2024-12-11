#!/bin/bash

# Logging function
log() {
    logger -t dwd_station_reference_update "$1"
}

BASE_PATH=$(dirname "$(realpath "$0")")

log "Starting dwd_station_reference_update process"

# Run SQL script to create temporary table and modify schema
log "Creating temporary table and modifying schema"
psql -U oklab -h localhost -d oklab -p 5432 <<EOF
BEGIN;

-- Create a temporary table
CREATE TABLE IF NOT EXISTS temp_dwd_station_reference AS SELECT * FROM dwd_station_reference WHERE false;

-- Execute schema modifications
\i $BASE_PATH/../data/dwd_station_references_schema.sql;
COMMIT;
EOF
log "Temporary table created and schema updated"

# Navigate to BASE_PATH
cd "$BASE_PATH/../tools" || { log "Failed to navigate to $BASE_PATH"; exit 1; }

# Activate the Python environment
log "Activating Python virtual environment"
python3 -m venv venv
source venv/bin/activate

# Run the Python script to insert data into the temporary table
log "Running Python script for data insertion"
pip3 install -r requirements.txt
python3 insert_weather_reference.py --env ../.env --url https://www.dwd.de/DE/leistungen/klimadatendeutschland/statliste/statlex_html.html\?view\=nasPublication\&nn\=16102 --verbose || log "Python script failed"

# Deactivate the Python environment
deactivate
log "Python virtual environment deactivated"

# Replace the original table with the temporary table
log "Replacing original table with temporary table"
psql -U oklab -h localhost -d oklab -p 5432 <<EOF
BEGIN;

-- Swap the temporary table with the original table
DROP TABLE IF EXISTS dwd_station_references;
ALTER TABLE temp_dwd_station_reference RENAME TO dwd_station_references;

COMMIT;
EOF
log "Replacement complete, dwd_station_reference_update process finished"
