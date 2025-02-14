# Open Data Ingestion Tools

This repository also provides tools to fetch, process, and insert various datasets into a PostgreSQL database. These tools are particularly useful for managing German administrative and energy-related data, such as municipality keys, energy unit metadata, and administrative areas.


---


## Insert Municipality Keys

This tool fetches and inserts official German municipality keys into a PostgreSQL database.


---


### Prerequisites

1. **Database Setup**

- Ensure PostgreSQL is installed and running on `localhost` (default port: `5432`).
- Create a database named `oklab`, owned by a user with the same name.
- Make sure the database accepts connections from `localhost`.

2. **Environment Variables**

- Create a `.env` file in the root directory of this repository and add the following environment variables with your specific values:

```sh
DB_PASS=YOUR_PASSWORD_HERE
DB_HOST=localhost
DB_USER=oklab
DB_NAME=oklab
DB_PORT=5432
```

3. **Python**

- Python 3 installed with `venv` and `pip` available.


---


### Steps

1. Set up the database schema:

```sh
psql -U oklab -h localhost -d oklab -p 5432 < data/de_municipality_keys_schema.sql
```

2. Activate a Python virtual environment and install dependencies:

```sh
cd tools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. Run the script to insert municipality keys:

```sh
python3 insert_municipality_key.py \
    --env ../.env \
    --target ../data \
    --url https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:ags_2024-10-31/download/AGS_2024-10-31.json \
    --verbose
```

4. Deactivate the virtual environment:

```sh
deactivate
```

---


## Insert Energy Metadata

This tool fetches and inserts wind turbine and solar energy metadata into your PostgreSQL database.


### Prerequisites

Ensure the database and Python environment are set up as described in the **Insert Municipality Keys** section.


### Steps

1. Set up the database schema:

```sh
psql -U oklab -h localhost -d oklab -p 5432 < data/de_energy_meta_schema.sql
```

2. Activate a Python virtual environment and install dependencies:

```sh
cd tools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. Run the script to insert energy metadata:

```sh
python3 insert_energy_meta.py \
    --env ../.env \
    --target ~ \
    --url https://www.marktstammdatenregister.de/MaStR/Einheit/EinheitJson/GetFilterColumnsErweiterteOeffentlicheEinheitStromerzeugung \
    --verbose
```

4. Deactivate the virtual environment:

```sh
deactivate
```

---


## Retrieve and Insert Energy Units

This tool processes data from the German energy market data register to insert various energy unit types (e.g., wind, solar, nuclear) into your PostgreSQL database.


### Prerequisites

1. Download the complete public data extract from the [German Energy Market Data Register](https://www.marktstammdatenregister.de/MaStR/Datendownload) and unpack the zip archive.

2. Set up the database schema for each energy unit type:

```sh
psql -U oklab -h localhost -d oklab -p 5432 < data/de_biomass_units_schema.sql
psql -U oklab -h localhost -d oklab -p 5432 < data/de_combustion_units_schema.sql
psql -U oklab -h localhost -d oklab -p 5432 < data/de_nuclear_units_schema.sql
psql -U oklab -h localhost -d oklab -p 5432 < data/de_solar_units_schema.sql
psql -U oklab -h localhost -d oklab -p 5432 < data/de_water_units_schema.sql
psql -U oklab -h localhost -d oklab -p 5432 < data/de_wind_units_schema.sql
```

### Steps

For each energy unit type, follow these steps:

1. Activate a Python virtual environment and install dependencies:

```sh
cd tools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

2. Run the script for the respective energy unit type. For example:

```sh
python3 insert_biomass_units.py --env ../.env --src ~/EinheitenBiomasse.xml --verbose
python3 insert_combustion_units.py --env ../.env --src ~/EinheitenVerbrennung.xml --verbose
python3 insert_nuclear_units.py --env ../.env --src ~/EinheitenKernkraft.xml --verbose
python3 insert_solar_units.py --env ../.env --src ~/EinheitenSolar_1.xml --verbose
python3 insert_water_units.py --env ../.env --src ~/EinheitenWasser.xml --verbose
python3 insert_wind_units.py --env ../.env --src ~/EinheitenWind.xml --verbose
```

3. Deactivate the virtual environment:

```sh
deactivate
```

---


## Retrieve Administrative Areas

Download administrative area data with population figures from the [Federal Agency for Cartography and Geodesy](https://gdz.bkg.bund.de/index.php/default/verwaltungsgebiete-1-250-000-mit-einwohnerzahlen-stand-31-12-vg250-ew-31-12.html). Use the `ogr2ogr` tool to insert this data into your PostgreSQL database.


### Steps

1. Download and unpack the administrative area dataset:

```sh
wget https://daten.gdz.bkg.bund.de/produkte/vg/vg250-ew_ebenen_1231/aktuell/vg250-ew_12-31.utm32s.gpkg.ebenen.zip
unzip vg250-ew_12-31.utm32s.gpkg.ebenen.zip
cd vg250-ew_12-31.utm32s.gpkg.ebenen/vg250-ew_ebenen_1231
```

2. Insert data into your database using `ogr2ogr`:

```sh
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=NO \
    -t_srs EPSG:4326 -nlt MULTIPOLYGON -overwrite -update DE_VG250.gpkg vg250_gem
```

```sh
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=NO \
    -t_srs EPSG:4326 -nlt MULTIPOLYGON -overwrite -update DE_VG250.gpkg vg250_krs
```

```sh
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=NO \
    -t_srs EPSG:4326 -nlt MULTIPOLYGON -overwrite -update DE_VG250.gpkg vg250_lan
```

```sh
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=NO \
    -t_srs EPSG:4326 -nlt MULTIPOLYGON -overwrite -update DE_VG250.gpkg vg250_rbz
```

```sh
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=NO \
    -t_srs EPSG:4326 -nlt MULTIPOLYGON -overwrite -update DE_VG250.gpkg vg250_sta
```

```sh
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=NO \
    -t_srs EPSG:4326 -nlt MULTIPOLYGON -overwrite -update DE_VG250.gpkg vg250_vwg
```

```sh
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=NO \
    -t_srs EPSG:4326 -nlt LINESTRING -overwrite -update DE_VG250.gpkg vg250_li
```

```sh
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=NO \
    -t_srs EPSG:4326 -nlt POINT -overwrite -update DE_VG250.gpkg vg250_pk
```


3. Next it is recommanded to create indecies using `psql`:

```sql
-- index state, county and municipality ids
CREATE INDEX IF NOT EXISTS idx_lan_sn_l ON vg250_lan (sn_l);
CREATE INDEX IF NOT EXISTS idx_krs_sn_l ON vg250_krs (sn_l);
CREATE INDEX IF NOT EXISTS idx_krs_sn_r ON vg250_krs (sn_r);
CREATE INDEX IF NOT EXISTS idx_krs_sn_k ON vg250_krs (sn_k);
CREATE INDEX IF NOT EXISTS idx_gem_sn_k ON vg250_gem (sn_k);
CREATE INDEX IF NOT EXISTS idx_gem_sn_r ON vg250_gem (sn_r);
CREATE INDEX IF NOT EXISTS idx_gem_sn_l ON vg250_gem (sn_l);

-- index for the municipality key
CREATE INDEX IF NOT EXISTS idx_vg250_gem_ags ON vg250_gem (ags);

-- index state names
CREATE INDEX IF NOT EXISTS idx_vg250_lan_gen ON vg250_lan (gen);

-- index on geofactor
CREATE INDEX IF NOT EXISTS idx_vg250_gem_gf ON vg250_gem (gf);
CREATE INDEX IF NOT EXISTS idx_vg250_krs_gf ON vg250_krs (gf);
CREATE INDEX IF NOT EXISTS idx_vg250_lan_gf ON vg250_lan (gf);

-- index place and admin level
CREATE INDEX IF NOT EXISTS idx_osm_point_place ON planet_osm_point (place);
CREATE INDEX IF NOT EXISTS idx_osm_polygon_admin_level ON planet_osm_polygon (admin_level);
```


4. Create a materialized view for faster search

> Note that materialized views need to be refreshed to update their content if the underlying data changes. After restoring, you may need to run:

```sql
REFRESH MATERIALIZED VIEW your_materialized_view_name;
```

> In case you want to drop an existing materialized view run:

```sql
DROP MATERIALIZED VIEW IF EXISTS mv_de_geographical_regions CASCADE;
```

> To create the materialized view run:

```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_de_geographical_regions AS
SELECT DISTINCT ON (point.name, gem.ags)
    REPLACE(point.name, 'Sankt ', 'St. ') AS geographical_name,
    CASE
        WHEN point.name != gem.gen AND point.place IN ('suburb', 'village', 'isolated_dwelling', 'hamlet', 'island', 'neighbourhood', 'quarter') THEN gem.bez || ' ' || REPLACE(gem.gen, 'Sankt ', 'St. ')
        WHEN point.name = gem.gen AND point.place IN ('suburb', 'village', 'isolated_dwelling', 'hamlet', 'island', 'neighbourhood', 'quarter') THEN krs.bez || ' ' || krs.gen
        WHEN point.place IN ('municipality', 'city', 'town') AND gem.ibz != 60 AND gem.ibz != 61 THEN krs.bez || ' ' || krs.gen
        ELSE lan.gen
    END AS region_name,
    gem.ags AS municipality_key
FROM
    planet_osm_point AS point
JOIN
    planet_osm_polygon AS poly
ON
    ST_Contains(poly.way, point.way)
JOIN
    vg250_gem AS gem
ON
    ST_Contains(gem.geom, ST_Transform(point.way, 4326)) AND gem.gf = 4
JOIN
    vg250_krs AS krs
ON
    gem.sn_l = krs.sn_l AND gem.sn_r = krs.sn_r AND gem.sn_k = krs.sn_k AND krs.gf = 4
JOIN
    vg250_lan AS lan
ON
    krs.sn_l = lan.sn_l
WHERE
    point.place IN ('municipality', 'suburb', 'city', 'town', 'village', 'isolated_dwelling', 'hamlet', 'island', 'neighbourhood', 'quarter')
    AND point.name IS NOT NULL
    AND poly.admin_level = '6';
```


5. Create indecies for this view

> The indexing only need to be done if you want to work on the materialized view. Make sure to create extionsion before creating indecies.

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```


```sql
-- index for comparison based on column
CREATE INDEX IF NOT EXISTS idx_mv_geographical_name ON mv_de_geographical_regions (geographical_name);
CREATE INDEX IF NOT EXISTS idx_mv_municipality_key ON mv_de_geographical_regions (municipality_key);
CREATE INDEX IF NOT EXISTS idx_mv_region_name ON mv_de_geographical_regions (region_name);

-- index for search based on ngram
CREATE INDEX IF NOT EXISTS idx_gin_mv_gr_geographical_name_lower ON mv_de_geographical_regions USING gin (LOWER(geographical_name) gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_gin_mv_gr_region_name_lower ON mv_de_geographical_regions USING gin (LOWER(region_name) gin_trgm_ops);
```


6. To dump the materialized view

```bash
psql -U oklab -h localhost -d oklab -p 5432 -c "DROP TABLE IF EXISTS de_geographical_regions"
psql -U oklab -h localhost -d oklab -p 5432 -c "CREATE TABLE IF NOT EXISTS de_geographical_regions AS TABLE mv_de_geographical_regions"
pg_dump -U oklab -d oklab -t de_geographical_regions --inserts > ~/de_geographical_regions.sql
psql -U oklab -h localhost -d oklab -p 5432 -c "DROP TABLE IF EXISTS de_geographical_regions"
```


7. To restore the dumped materialized view

```bash
psql -U oklab -h localhost -d oklab -p 5432 -c "DROP TABLE IF EXISTS de_geographical_regions"
psql -U oklab -h localhost -d oklab -p 5432 -f ~/de_geographical_regions.sql
psql -U oklab -h localhost -d oklab -p 5432 -c "CREATE INDEX IF NOT EXISTS idx_gin_geographical_name_lower ON de_geographical_regions USING gin (LOWER(geographical_name) gin_trgm_ops);"
psql -U oklab -h localhost -d oklab -p 5432 -c "CREATE INDEX IF NOT EXISTS idx_gin_region_name_lower ON de_geographical_regions USING gin (LOWER(region_name) gin_trgm_ops);"
```



## Retrieve German Weather Stations

This tool downloads and processes data about German weather stations and inserts it into a PostgreSQL database.


### Prerequisites

1. Environment Variables:
   Ensure that you have created the `.env` file as described in previous sections.

2. Python:
   Install Python 3 with `venv` and `pip`, if not already done.

3. Wget:
   Install `wget` to download the source file.


---


### Steps


1. Download Weather Station Data:

Use the following command to download the list of German weather stations:

```sh
wget https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/KL_Tageswerte_Beschreibung_Stationen.txt
```

This will download a file named `KL_Tageswerte_Beschreibung_Stationen.txt` to your current working directory.


2. Activate Virtual Environment and Install Dependencies:

If you haven’t done so already, activate your Python virtual environment and install the required dependencies:

```sh
cd tools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```


3. **Insert Data into PostgreSQL Database**:

Run the following command to insert the weather station data into the database:

```sh
python3 insert_weather_stations.py --env ../.env --src ~/KL_Tageswerte_Beschreibung_Stationen.txt --verbose
```

**Parameters:**
- `--env ../.env`: Path to the environment variable file.
- `--src ~/KL_Tageswerte_Beschreibung_Stationen.txt`: Path to the downloaded file.
- `--verbose`: Optional flag to enable detailed logging output.


4. Deactivate Virtual Environment:

Deactivate the Python environment when you're finished:

```sh
deactivate
```

---


## Insert EU Country Codes

This tool fetches and inserts EU country code data into your PostgreSQL database.


### Prerequisites

1. Database Setup

- Ensure PostgreSQL is installed and running on `localhost` (default port: `5432`).
- Create a database named `oklab`, owned by a user with the same name.
- Ensure the database is accessible from `localhost`.


2. **Environment Variables**

- Create a `.env` file in the root directory of this repository and add the following environment variables with your specific values:

```sh
DB_PASS=YOUR_PASSWORD_HERE
DB_HOST=localhost
DB_USER=oklab
DB_NAME=oklab
DB_PORT=5432
```


3. Python

- Ensure Python 3 is installed with `venv` and `pip` available.


---


### Steps

1. Set up the database schema:

Use the following command to create the necessary schema for EU country codes in the database:

```sh
psql -U oklab -h localhost -d oklab -p 5432 < data/eu_country_codes_schema.sql
```

This will execute the `eu_country_codes_schema.sql` script to create the necessary tables and schema in the PostgreSQL database.


2. Set up a Python virtual environment and install dependencies:

Navigate to the `tools` directory and create a virtual environment. Then, activate it and install the required Python dependencies:

```sh
cd tools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```


3. Insert EU country codes into the database:

Run the script to insert the country codes from the `eu_country_codes.csv` file into the PostgreSQL database:

```sh
python3 insert_country_codes.py --env ../.env --src ../data/eu_country_codes.csv --verbose
```

**Parameters:**

- `--env ../.env`: Path to the environment variable file.
- `--src ../data/eu_country_codes.csv`: Path to the CSV file containing the country codes.
- `--verbose`: Optional flag to enable detailed logging output.


4. Deactivate the virtual environment:

Once the script has run successfully, deactivate the Python virtual environment:

```sh
deactivate
```

---


## Insert Weather Station Reference

This section describes how to set up and insert weather station reference data into your PostgreSQL database.


---


### Prerequisites

1. **Database Schema Setup**:

Ensure that the PostgreSQL database schema for weather station reference is set up. Use the following command:

```sh
psql -U oklab -h localhost -d oklab -p 5432 < data/de_weather_stations_schema.sql
psql -U oklab -h localhost -d oklab -p 5432 < data/dwd_station_reference_schema.sql
psql -U oklab -h localhost -d oklab -p 5432 < data/dwd_abbreviations_schema.sql
```


2. **Environment Variables**:

Create a `.env` file in the root directory with the following content:

```sh
DB_PASS=YOUR_PASSWORD_HERE
DB_HOST=localhost
DB_USER=oklab
DB_NAME=oklab
DB_PORT=5432
```


3. **Python Setup**:

Ensure Python 3 is installed with `venv` and `pip`.


---


### Steps

1. **Set Up the Python Environment**:

Navigate to the `tools` directory and set up a Python virtual environment:

```sh
cd tools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```


2. **Insert Weather Station Reference**:

Run the following command to insert weather station reference data from the provided URL into your database:

> Note you may find the lates url at [DWD Stationslexikon](https://www.dwd.de/DE/leistungen/klimadatendeutschland/stationsliste.html) under the section `Stationslexikon im HTML-Format`.

```sh
python3 insert_weather_reference.py --env ../.env --url https://www.dwd.de/DE/leistungen/klimadatendeutschland/statliste/statlex_html.html\?view\=nasPublication\&nn\=16102 --verbose
```

**Parameters:**

- `--env ../.env`: Path to the `.env` file with database credentials.
- `--url`: URL to the data source.
- `--verbose`: Optional flag for detailed logging output.


3. **Deactivate the Python Environment**:

Once the script has completed, deactivate the Python environment:

```sh
deactivate
```


---


## Insert archaeological monuments

> This section will guide your team through the necessary steps to download and load the archaeological monument data into the database.


1. **Find the Latest JSON URL for "Denkmalliste unbeweglicher archäologischer Kulturdenkmale"**

- Go to the [Open Data Schleswig-Holstein site](https://opendata.schleswig-holstein.de).
- Find the latest dataset titled **"Denkmalliste unbeweglicher archäologischer Kulturdenkmale"** and get the latest JSON download URL.


2. **Create the Required Database Table**

Run the following command from the root of the repo to create the necessary schema in your PostgreSQL database:

```bash
psql -U oklab -h localhost -d oklab -p 5432 < data/sh_archaeological_monument_schema.sql
```


3. **Create `.env` File (If Not Already Created)**

Ensure a `.env` file exists in the root directory of the `open-data-api` repository with the following content:

```bash
DB_PASS=oklab
DB_HOST=localhost
DB_USER=oklab
DB_NAME=oklab
DB_PORT=5432
```


4. **Set Up Python Environment**

- Navigate to the `tools` directory:

```bash
cd tools
```

- Activate the virtual environment:

```bash
source venv/bin/activate
```

- Install the necessary dependencies:
     
```bash
pip3 install -r requirements.txt
```


5. **Insert Archaeological Monuments Data**

Use the following command to fetch and insert the data into the database. Replace the `--url` parameter with the latest JSON URL if necessary:

```bash
python3 insert_archaeological_monuments.py --env ../.env --target ../data --url https://opendata.schleswig-holstein.de/dataset/7db5bc2f-7a99-456b-9faa-005de581cceb/resource/e0157633-62f6-43a0-8f89-3d4aef75801f/download/denkmalliste_sh.json --verbose
```


6. **Deactivate the Virtual Environment**

Once the script finishes, deactivate the virtual environment:

```bash
deactivate
```


7. **Navigate Back to the Root Directory of the Repo**

```bash
cd ..
```
