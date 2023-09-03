# OK Lab Flensburg OpenAPI


Prepare yourself and follow these instructions

```
sudo apt install git virtualenv python3 python3-pip postgresql-15 postgresql-15-postgis-3 postgis
```


Create dot `.env` file and add the following vars with `vim .env`

```
DB_PASS=postgres
DB_HOST=localhost
DB_USER=postgres
DB_NAME=postgres
DB_PORT=5432
```


Make sure to import sql statements from `open-social-map`

```
git clone https://github.com/oklabflensburg/open-social-map.git
cd open-social-map
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
psql -U postgres -h localhost -d postgres -p 5432 < data/cleanup_database_schema.sql
psql -U postgres -h localhost -d postgres -p 5432 < data/flensburg_sozialatlas_metadaten.sql
./insert_geography.py data/flensburg_stadtteile.geojson
deactivate
cd ..
```


Next initialize the virtualenv and install the dependencies

```
git clone https://github.com/oklabflensburg/open-data-api.git
cd open-data-api
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```


Now start the api service and test all routes

```sql
uvicorn main:app --reload
```


## LICENSE

[CC0-1.0](LICENSE)
