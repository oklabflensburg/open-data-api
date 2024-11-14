# Open Data API

> This API endpoints are open to everyone and please use GitHub issues to report or request anything.

![Screenshot Documentation](https://raw.githubusercontent.com/oklabflensburg/open-data-api/main/screenshot_open_data_api.jpg)


## API host

[https://api.oklabflensburg.de](https://api.oklabflensburg.de/docs)


## Prerequisites

If you wih to run your own instance of this open data API follow these steps. First you may want to install system dependencies for your Ubuntu machine.

```sh
sudo apt update
sudo apt install wget
sudo apt install git git-lfs
sudo apt install python3 python3-pip python3-venv
sudo apt install postgresql-16 postgresql-postgis gdal-bin
```


## Creating Dedicated User Accounts

The Open Data API will run as a global service on your machine. It is therefore best to install it under its own separate user account. In the following we assume this user is called `oklab` and the installation will be in `/srv/oklab`. To create the user and directory run:

```
sudo adduser oklab
sudo usermod -a -G www-data oklab
sudo mkdir -p /srv/oklab
sudo chown -R oklab:oklab /srv/oklab
sudo chmod 770 -R /srv/oklab
```


## Prepare Database

Open and edit `/etc/postgresql/16/main/pg_hba.conf` add following two entries into your config.

```
local   oklab           oklab                                   trust
host    oklab           oklab           127.0.0.1/32            trust
```

After these edits run `sudo systemctl restart postgresql.service`. To verify everything works run..

```
sudo systemctl status postgresql.service
```


Now change user `sudo -i -u postgres` and run these commands.

```
createuser -d oklab
createdb -O oklab oklab
psql -U oklab
exit
```

Note since the `oklab`-user does not have superuser permissions you must login with the `postgres` user.

```
psql -U postgres
\c oklab

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS hstore;

ALTER TABLE geography_columns OWNER TO oklab;
ALTER TABLE geometry_columns OWNER TO oklab;
ALTER TABLE spatial_ref_sys OWNER TO oklab;

\q
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
DB_USER=oklab
DB_NAME=oklab
DB_PORT=5432
```


## Import data

To use the all open data API endpoints you may import following data

```sh
cd ..
git clone https://github.com/oklabflensburg/open-social-map.git
cd open-social-map
psql -U oklab -h localhost -d oklab -p 5432 < data/flensburg_stadtteile.sql
cp ../open-data-api/.env .
cd tools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 insert_districts.py ../static/flensburg_stadtteile.geojson
deactivate
psql -U oklab -h localhost -d oklab -p 5432 < data/flensburg_sozialatlas.sql
psql -U oklab -h localhost -d oklab -p 5432 < data/flensburg_sozialatlas_metadaten.sql
```

In case you messed up anything, you can run this line but be aware it will delete all tables

```
psql -U oklab -h localhost -d oklab -p 5432 < data/cleanup_database_schema.sql
```

After running this line you must repeat all steps above to import all data


```sh
cd ..
git clone https://github.com/oklabflensburg/open-monuments-map.git
cd open-monuments-map
git lfs pull
psql -U oklab -h localhost -d oklab -p 5432 < data/denkmalliste_schema.sql
cp ../open-data-api/.env .
cd tools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 insert_boundaries.py ../data/denkmalliste_geometrien.geojson
python3 insert_monuments.py ../data/stadt-flensburg-denkmalschutz.geojson
deactivate
cd ..
```


Run the following commands to receive a propper result calling the monument open data API endpoints.

First add all German administrative geometries with `ogr2ogr`

```
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" "data/vg250gem.geojson" -nln vg250gem
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" "data/vg250vwg.geojson" -nln vg250vwg
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" "data/vg250krs.geojson" -nln vg250krs
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" "data/vg250lan.geojson" -nln vg250lan
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" "data/vg250rbz.geojson" -nln vg250rbz
ogr2ogr -f "PostgreSQL" PG:"dbname=oklab user=oklab port=5432 host=localhost" "data/vg250sta.geojson" -nln vg250sta
```


Run the following commands to receive a propper result calling the accident open data API endpoints.

```sh
cd ..
git clone https://github.com/oklabflensburg/open-accident-map.git
cd open-accident-map
git lfs pull
psql -U oklab -h localhost -d oklab -p 5432 < data/unfallorte_deutschland_schema.sql
cp ../open-data-api/.env .
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


## How to test

```
curl -X 'GET' 'http://localhost:8000/demographics/v1/details'  -H 'accept: application/json'
```


## Setup service

Congrats you are a hero you almost got the most. Now create a file `/usr/lib/systemd/system/open-data-api.service` and add these lines to your service file. Make sure to replace all custom stuff according your local machine setup.

```conf
[Unit]
Description=Instance to serve the open data api
After=network.target
Requires=postgresql.service

[Service]
Type=simple
User=oklab
Group=www-data
DynamicUser=true

WorkingDirectory=/srv/oklab/open-data-api
PrivateTmp=true

EnvironmentFile=/srv/oklab/open-data-api/.env
ExecStart=/srv/oklab/open-data-api/venv/bin/uvicorn \
        --proxy-headers \
        --forwarded-allow-ips='*' \
        --workers=4 \
        --port=6720 \
        main:app

ExecReload=/bin/kill -HUP ${MAINPID}
RestartSec=1
Restart=always

[Install]
WantedBy=multi-user.target
```

Now you may start and when there are no errors enable the service to boot after startup.

```
sudo systemctl start open-data-api.service
sudo systemctl status open-data-api.service
sudo systemctl enable open-data-api.service
```


## Setup webserver


Install dependencies on your machine.

```sh
sudo apt install nginx certbot python3-certbot-nginx
```


Make sure to harden your server according your needs, this is just our default setup.

```nginx
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;


# provides the configuration file context in which the directives that affect connection processing are specified.
events {
    # determines how much clients will be served per worker, max clients = worker_connections * worker_processes
    # max clients is also limited by the number of socket connections available on the system (~64k)
    worker_connections 1024;

    # optmized to serve many clients with each thread, essential for linux
    use epoll;

    # accept as many connections as possible, may flood worker connections if set too low
    multi_accept on;
}

http {
    log_format main '$remote_addr - $remote_user [$time_local] $status '
                    '"$host" "$request" $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    # copies data between one FD and other from within the kernel
    # faster then read() + write()
    sendfile on;

    # send headers in one peace, its better then sending them one by one
    tcp_nopush on;

    # don't buffer data sent, good for small data bursts in real time
    tcp_nodelay on;

    # How long to allow each connection to stay idle; longer values are better
    # for each individual client, particularly for SSL, but means that worker
    # connections are tied up longer. (Default: 65)
    keepalive_timeout 65;

    # allow the server to close connection on non responding client, this will free up memory
    reset_timedout_connection on;

    # Set the maximum size of the types hash tables
    types_hash_max_size 2048;

    # ciphers chosen for forward secrecy and compatibility
    # http://blog.ivanristic.com/2013/08/configuring-apache-nginx-and-openssl-for-forward-secrecy.html
    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';

    # enables server-side protection from BEAST attacks
    # http://blog.ivanristic.com/2013/09/is-beast-still-a-threat.html
    ssl_prefer_server_ciphers on;

    # disable SSLv3(enabled by default since nginx 0.8.19) since it's less secure then TLS
    # http://en.wikipedia.org/wiki/Secure_Sockets_Layer#SSL_3.0
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;

    # enable session resumption to improve https performance
    # http://vincent.bernat.im/en/blog/2011-ssl-session-reuse-rfc5077.html
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 5m;

    # Diffie-Hellman parameter for DHE ciphersuites, recommended 2048 bits
    ssl_dhparam /etc/ssl/private/dhparams.pem;

    # limit the number of connections per single IP
    limit_conn_zone $binary_remote_addr zone=conn_limit_per_ip:10m;

    # limit the number of requests for a given session
    limit_req_zone $binary_remote_addr zone=req_limit_per_ip:10m rate=5r/s;

    # if the request body size is more than the buffer size, then the entire (or partial) request body is written into a temporary file
    client_body_buffer_size 128k;

    # headerbuffer size for the request header from client, its set for testing purpose
    client_header_buffer_size 3m;

    # maximum number and size of buffers for large headers to read from client request
    large_client_header_buffers 4 256k;

    # read timeout for the request body from client, its set for testing purpose
    client_body_timeout 3m;

    # how long to wait for the client to send a request header, its set for testing purpose
    client_header_timeout 3m;

    # don't send the nginx version number in error pages and Server header
    server_tokens off;

    # config to don't allow the browser to render the page inside an frame or iframe
    # and avoid clickjacking http://en.wikipedia.org/wiki/Clickjacking
    # if you need to allow [i]frames, you can use SAMEORIGIN or even set an uri with ALLOW-FROM uri
    # https://developer.mozilla.org/en-US/docs/HTTP/X-Frame-Options
    add_header X-Frame-Options SAMEORIGIN;

    # when serving user-supplied content, include a X-Content-Type-Options: nosniff header along with the Content-Type: header,
    # to disable content-type sniffing on some browsers.
    # https://www.owasp.org/index.php/List_of_useful_HTTP_headers
    # currently suppoorted in IE > 8 http://blogs.msdn.com/b/ie/archive/2008/09/02/ie8-security-part-vi-beta-2-update.aspx
    # http://msdn.microsoft.com/en-us/library/ie/gg622941(v=vs.85).aspx
    # 'soon' on Firefox https://bugzilla.mozilla.org/show_bug.cgi?id=471020
    add_header X-Content-Type-Options nosniff;

    # This header enables the Cross-site scripting (XSS) filter built into most recent web browsers.
    # It's usually enabled by default anyway, so the role of this header is to re-enable the filter for
    # this particular website if it was disabled by the user.
    # https://www.owasp.org/index.php/List_of_useful_HTTP_headers
    add_header X-XSS-Protection "1; mode=block";

    # config to enable HSTS(HTTP Strict Transport Security)
    # https://developer.mozilla.org/en-US/docs/Security/HTTP_Strict_Transport_Security
    # to avoid ssl stripping https://en.wikipedia.org/wiki/SSL_stripping#SSL_stripping
    # add_header Strict-Transport-Security "max-age=15552000; includeSubdomains; preload";

    # with Content Security Policy (CSP) enabled(and a browser that supports it(http://caniuse.com/#feat=contentsecuritypolicy),
    # you can tell the browser that it can only download content from the domains you explicitly allow
    # http://www.html5rocks.com/en/tutorials/security/content-security-policy/
    # https://www.owasp.org/index.php/Content_Security_Policy
    # I need to change our application code so we can increase security by disabling 'unsafe-inline' 'unsafe-eval'
    # directives for css and js(if you have inline css or js, you will need to keep it too).
    # more: http://www.html5rocks.com/en/tutorials/security/content-security-policy/#inline-code-considered-harmful
    # add_header Content-Security-Policy "default-src 'self'; script-src 'unsafe-inline' 'unsafe-eval' https://unpkg.com; img-src 'self' data: https://tile.openstreetmap.org; style-src 'self' 'unsafe-inline' https://unpkg.com; font-src 'self'; worker-src 'none'; object-src 'none'";

    # opt-in to the future
    add_header "X-UA-Compatible" "IE=Edge";

    # Control the maximum length of a virtual host entry
    server_names_hash_bucket_size 128;

    # server_name_in_redirect off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging Settings
    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # Gzip Settings
    gzip on;
    gzip_vary on;
    gzip_proxied expired no-cache no-store private auth;
    gzip_comp_level 9;
    gzip_buffers 16 8k;
    gzip_http_version 1.1;
    gzip_types text/plain text/css application/octet-stream application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml image/jpeg image/webp image/png;

    # Virtual Host Configs
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```


Now setup Open Data API Webserver with HTTP2 configuration in `/etc/nginx/sites-enabled/default`.

```nginx
server {
  # listen 443 ssl http2;
  # listen [::]:443 ssl http2;
  server_name api.oklabflensburg.de;

  charset utf-8;
  add_header Content-Security-Policy "default-src 'self'; script-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; font-src 'self'; worker-src 'none'; object-src 'none'; connect-src 'self'";

  location ~ /\. {
    deny all;
  }

  location / {
    if ($request_method = 'OPTIONS') {
      add_header 'Access-Control-Allow-Origin' '*';
      #
      # Om nom nom cookies
      #
      add_header 'Access-Control-Allow-Credentials' 'true';
      add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';

      #
      # Custom headers and headers various browsers *should* be OK with but aren't
      #
      add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';

      #
      # Tell client that this pre-flight info is valid for 20 days
      #
      add_header 'Access-Control-Max-Age' 1728000;
      add_header 'Content-Type' 'text/plain charset=UTF-8';
      add_header 'Content-Length' 0;
      return 204;
    }

    if ($request_method = 'POST') {
      add_header 'Access-Control-Allow-Origin' '*';
      add_header 'Access-Control-Allow-Credentials' 'true';
      add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
      add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
    }

    if ($request_method = 'GET') {
      add_header 'Access-Control-Allow-Origin' '*';
      add_header 'Access-Control-Allow-Credentials' 'true';
      add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
      add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
    }

    proxy_pass http://localhost:6720;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;

    proxy_buffering on;
    proxy_cache_valid 200 5m;
    proxy_cache_use_stale error timeout invalid_header updating http_500 http_502 http_503 http_504;
    proxy_cache_bypass $http_cache_control;
    add_header X-Proxy-Cache $upstream_cache_status;
    add_header Strict-Transport-Security "max-age=15768000; includeSubDomains; preload" always;
  }

  listen 80;
}
```


## Test configuration

Test configuration and install certificates, make sure to uncomment `http2` after certbot run.

```sh
sudo nginx -t
sudo certbot
```


## Control webserver

```sh
sudo systemctl start nginx.service
sudo systemctl status nginx.service
sudo systemctl enable nginx.service
```


## Insert municipality keys

Tool to fetch and insert offical german municipality keys

```sh
psql -U oklab -h localhost -d oklab -p 5432 < ../data/de_official_municipality_keys_schema.sql
```

```sh
cd tools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 insert_municipality_key.py --env ../.env --target ../data --url https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:ags_2024-10-31/download/AGS_2024-10-31.json --verbose
deactivate
```


## Insert energy units

Tool to insert solar energy units from local file system.

```sh
cd tools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 insert_solar_units.py --env ../.env --src ~/EinheitenSolar_1.xml --verbose
deactivate
```



## Retrieve administrative areas

Download latest administrative areas 1:250,000 with population figures (VG250-EW) from the [Federal Agency for Cartography and Geodesy](https://gdz.bkg.bund.de/index.php/default/verwaltungsgebiete-1-250-000-mit-einwohnerzahlen-stand-31-12-vg250-ew-31-12.html).

```sh
wget https://daten.gdz.bkg.bund.de/produkte/vg/vg250-ew_ebenen_1231/aktuell/vg250-ew_12-31.utm32s.shape.ebenen.zip
unzip vg250-ew_12-31.utm32s.shape.ebenen.zip
cd vg250-ew_12-31.utm32s.shape.ebenen/vg250-ew_ebenen_1231
```

```sh
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES -nlt POLYGON -s_srs VG250_GEM.prj -t_srs EPSG:4326 VG250_GEM.shp
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES -nlt POLYGON -s_srs VG250_KRS.prj -t_srs EPSG:4326 VG250_KRS.shp
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES -nlt POLYGON -s_srs VG250_LAN.prj -t_srs EPSG:4326 VG250_LAN.shp
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES -nlt POLYGON -s_srs VG250_RBZ.prj -t_srs EPSG:4326 VG250_RBZ.shp
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES -nlt POLYGON -s_srs VG250_STA.prj -t_srs EPSG:4326 VG250_STA.shp
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES -nlt POLYGON -s_srs VG250_VWG.prj -t_srs EPSG:4326 VG250_VWG.shp
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES -nlt LINESTRING -s_srs VG250_LI.prj -t_srs EPSG:4326 VG250_LI.shp
ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=oklab user=oklab" -lco GEOMETRY_NAME=geom -lco SPATIAL_INDEX=GIST -lco PRECISION=YES -nlt POINT -s_srs VG250_PK.prj -t_srs EPSG:4326 VG250_PK.shp
```



## How to contribute

You are welcome to contribute to the open data API. You may have a look in our [CONTRIBUTING.md](CONTRIBUTING.md) guide.



## LICENSE

[CC0-1.0](LICENSE)
