# Open Data API

> This API endpoints are open to everyone and please use GitHub issues to report or request anything.

![Screenshot Documentation](https://raw.githubusercontent.com/oklabflensburg/open-data-api/main/screenshot_open_data_api.jpg)


## API host

[https://api.oklabflensburg.de](https://api.oklabflensburg.de/docs)


## Prerequisites

If you wih to run your own instance of this open data API follow these steps. First you may want to install system dependencies for your Ubuntu machine.

```sh
sudo apt install git git-lfs
sudo apt install python3 python3-pip python3-venv
sudo apt install postgresql-16 postgis-3 gdal-bin
```


## Repository

To run your own instance of the open data API, first clone the repository and initialize a python virtualenv and install application dependencies.

```sh
git clone https://github.com/oklabflensburg/open-data-api.git
cd open-data-api
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
deactivate
```


Next you may create a dot `.env` file and add the following enviroment variables with your values.

```sh
DB_PASS=postgres
DB_HOST=localhost
DB_USER=postgres
DB_NAME=postgres
DB_PORT=5432
```


## Import data

To use the all open data API endpoints you may import following data

```sh
cd ..
git clone https://github.com/oklabflensburg/open-social-map.git
cd open-social-map
sudo -i -Hu postgres psql -U postgres -h localhost -d postgres -p 5432 < data/cleanup_database_schema.sql
sudo -i -Hu postgres psql -U postgres -h localhost -d postgres -p 5432 < data/flensburg_sozialatlas.sql
sudo -i -Hu postgres psql -U postgres -h localhost -d postgres -p 5432 < data/flensburg_sozialatlas_metadaten.sql
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 insert_districts.py ../static/flensburg_stadtteile.geojson
deactivate
```

Run the following commands to receive a propper result calling the monument open data API endpoints.

First add all German administrative geometries with `ogr2ogr`

```
ogr2ogr -f "PostgreSQL" PG:"dbname=postgres user=postgres port=5432 host=localhost" "data/vg250gem.geojson" -nln vg250gem
ogr2ogr -f "PostgreSQL" PG:"dbname=postgres user=postgres port=5432 host=localhost" "data/vg250vwg.geojson" -nln vg250vwg
ogr2ogr -f "PostgreSQL" PG:"dbname=postgres user=postgres port=5432 host=localhost" "data/vg250krs.geojson" -nln vg250krs
ogr2ogr -f "PostgreSQL" PG:"dbname=postgres user=postgres port=5432 host=localhost" "data/vg250lan.geojson" -nln vg250lan
ogr2ogr -f "PostgreSQL" PG:"dbname=postgres user=postgres port=5432 host=localhost" "data/vg250rbz.geojson" -nln vg250rbz
ogr2ogr -f "PostgreSQL" PG:"dbname=postgres user=postgres port=5432 host=localhost" "data/vg250sta.geojson" -nln vg250sta
```

```sh
cd ..
git clone https://github.com/oklabflensburg/open-monuments-map.git
cd open-monuments-map
git lfs pull
sudo -i -Hu postgres psql -U postgres -h localhost -d postgres -p 5432 < data/denkmalliste_schema.sql
cd tools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 insert_boundaries.py ../data/denkmalliste_geometrien.geojson
python3 insert_monuments.py ../data/stadt-flensburg-denkmalschutz.geojson
deactivate
cd ..
```

Run the following commands to receive a propper result calling the accident open data API endpoints.

```sh
cd ..
git clone https://github.com/oklabflensburg/open-accident-map.git
cd open-accident-map
git lfs pull
sudo -i -Hu postgres psql -U postgres -h localhost -d postgres -p 5432 < data/unfallorte_deutschland_schema.sql
cd tools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
for i in {16..22}; do python3 insert_accidents.py ../data/accidents_20$i.geojson; done
deactivate
cd ..
```


## How to use

Now you should be ready start the open data API loacally and test all routes

```sh
cd ../open-data-api
source venv/bin/activate
uvicorn main:app --reload
```


## How to contribute

You are welcome to contribute to the open data API. You may have a look in our [CONTRIBUTING.md](CONTRIBUTING.md) guide.



## LICENSE

[CC0-1.0](LICENSE)
