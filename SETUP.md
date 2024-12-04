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
psql -U oklab -h localhost -d oklab -p 5432 < data/de_official_municipality_keys_schema.sql
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
wget https://daten.gdz.bkg.bund.de/produkte/vg/vg250-ew_ebenen_1231/aktuell/vg250-ew_12-31.utm32s.shape.ebenen.zip
unzip vg250-ew_12-31.utm32s.shape.ebenen.zip
cd vg250-ew_12-31.utm32s.shape.ebenen/vg250-ew_ebenen_1231
```

2. Insert data into your database using `ogr2ogr`:

```sh
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES \
    -nlt POLYGON -s_srs VG250_GEM.prj -t_srs EPSG:4326 VG250_GEM.shp
```

```sh
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES \
    -nlt POLYGON -s_srs VG250_KRS.prj -t_srs EPSG:4326 VG250_KRS.shp
```

```sh
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES \
    -nlt POLYGON -s_srs VG250_LAN.prj -t_srs EPSG:4326 VG250_LAN.shp
```

```sh
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES \
    -nlt POLYGON -s_srs VG250_RBZ.prj -t_srs EPSG:4326 VG250_RBZ.shp
```

```sh
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES \
    -nlt POLYGON -s_srs VG250_STA.prj -t_srs EPSG:4326 VG250_STA.shp
```

```sh
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES \
    -nlt POLYGON -s_srs VG250_VWG.prj -t_srs EPSG:4326 VG250_VWG.shp
```

```sh
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES \
    -nlt LINESTRING -s_srs VG250_LI.prj -t_srs EPSG:4326 VG250_LI.shp
```

```sh
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" \
    -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES \
    -nlt POINT -s_srs VG250_PK.prj -t_srs EPSG:4326 VG250_PK.shp
```


3. Next it is recommanded to create indecies using `psql`:

```sql
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

-- index for gin ngram
CREATE INDEX IF NOT EXISTS idx_osm_point_place ON planet_osm_point (place);
CREATE INDEX IF NOT EXISTS idx_osm_polygon_admin_level ON planet_osm_polygon (admin_level);
CREATE INDEX IF NOT EXISTS idx_gin_osm_polygon_name_lower ON planet_osm_polygon USING gin (LOWER(name) gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_gin_osm_point_name_lower ON planet_osm_point USING gin (LOWER(name) gin_trgm_ops);
```


4. Create a materialized view for faster search

```sql
SELECT DISTINCT ON (point.name, gem.ags)
    REPLACE(point.name, 'Sankt ', 'St. ') AS geographical_name,
    CASE
        WHEN point.name != gem.gen AND point.place IN ('suburb', 'village', 'isolated_dwelling', 'hamlet', 'island', 'neighbourhood', 'quarter')  THEN gem.bez || ' ' || REPLACE(gem.gen, 'Sankt ', 'St. ')
        WHEN point.name = gem.gen AND point.place IN ('suburb', 'village', 'isolated_dwelling', 'hamlet', 'island', 'neighbourhood', 'quarter')  THEN krs.bez || ' ' || krs.gen
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

```sql
-- index for comparison based on column
CREATE INDEX IF NOT EXISTS idx_mv_geographical_name ON mv_geographical_regions (geographical_name);
CREATE INDEX IF NOT EXISTS idx_mv_municipality_key ON mv_geographical_regions (municipality_key);
CREATE INDEX IF NOT EXISTS idx_mv_region_name ON mv_geographical_regions (region_name);

-- index for search based on ngram
CREATE INDEX IF NOT EXISTS idx_gin_mv_gr_geographical_name_lower ON mv_geographical_regions USING gin (LOWER(geographical_name) gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_gin_mv_gr_region_name_lower ON mv_geographical_regions USING gin (LOWER(region_name) gin_trgm_ops);
```