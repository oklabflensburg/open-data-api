# Open Data API

> This API endpoints are open to everyone and please use GitHub issues to report or request anything.

![Screenshot Documentation](https://raw.githubusercontent.com/oklabflensburg/open-data-api/main/screenshot_open_data_api.jpg)


## API host

[https://api.oklabflensburg.de](https://api.oklabflensburg.de/docs)


## Prerequisites

If you wih to run your own instance of this open data API follow these steps. First you may want to install system dependencies for your Ubuntu machine.

```sh
sudo apt install git virtualenv python3 python3-pip postgresql-15 postgresql-15-postgis-3 postgis
```


## Repository

To run your own instance of the open data API, first clone the repository and initialize a python virtualenv and install application dependencies.

```sh
git clone https://github.com/oklabflensburg/open-data-api.git
cd open-data-api
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
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
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
psql -U postgres -h localhost -d postgres -p 5432 < data/cleanup_database_schema.sql
psql -U postgres -h localhost -d postgres -p 5432 < data/flensburg_sozialatlas_metadaten.sql
./insert_geography.py data/flensburg_stadtteile.geojson
deactivate
```


## How to use

Now you should be ready start the open data API loacally and test all routes

```sh
cd ../open-data-api
source venv/bin/activate
uvicorn main:app --reload
```


## Contribute

You are welcome to contribute to the open data API. You may have a look in our [CONTRIBUTING.md](CONTRIBUTING.md) guide.



## LICENSE

[CC0-1.0](LICENSE)
