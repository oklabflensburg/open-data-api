import os
import re
import sys
import json
import click
import hashlib
import traceback
import logging as log
import psycopg2
import psycopg2.extras
import httpx

from shapely import wkt
from shapely.ops import transform
from shapely.geometry import MultiPolygon
from geoalchemy2.shape import from_shape
from pyproj import Transformer
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv
from pathlib import Path



# log uncaught exceptions
def log_exceptions(type, value, tb):
    for line in traceback.TracebackException(type, value, tb).format(chain=True):
        log.exception(line)

    log.exception(value)

    sys.__excepthook__(type, value, tb) # calls default excepthook


def connect_database(env_path):
    try:
        load_dotenv(dotenv_path=Path(env_path))

        conn = psycopg2.connect(
            database = os.getenv('DB_NAME'),
            password = os.getenv('DB_PASS'),
            user = os.getenv('DB_USER'),
            host = os.getenv('DB_HOST'),
            port = os.getenv('DB_PORT')
        )

        conn.autocommit = True

        log.info('connection to database established')

        return conn
    except Exception as e:
        log.error(e)

        sys.exit(1)


def parse_geometry(geometry_wkt):
    # Extract SRID and WKT geometry
    srid, wkt_geometry = geometry_wkt.split(';')
    srid = int(srid.replace('SRID=', ''))

    # Convert WKT to Shapely geometry
    shape = wkt.loads(wkt_geometry)

    # Transform CRS to EPSG:4326
    transformer = Transformer.from_crs(f"EPSG:{srid}", "EPSG:4326", always_xy=True)
    transformed_shape = transform(transformer.transform, shape)

    # Ensure it's a MultiPolygon
    if not isinstance(transformed_shape, MultiPolygon):
        transformed_shape = MultiPolygon([transformed_shape])

    return transformed_shape


def parse_json(conn, data):
    cur = conn.cursor()

    for entries in data:
        for entry in entries['akd']:
            insert_row(cur, entry)


def insert_row(cur, row):
    object_name = row.get('objektbezeichnung')
    proper_name = row.get('eigenname')        
    object_number = row.get('objektnummer')
    district_name = row.get('kreis')             
    municipality_name = row.get('gemeinde')         
    object_description = row.get('objektbeschreibung')
    object_significance = row.get('objektbegruendung')
    protection_scope = row.get('schutzumfang')        
    date_registered = row.get('datum_eintragung')
    date_modified = row.get('datum_aenderung')
    status = row.get('status')
    heritage_authority = row.get('untere_denkmalschutzbehoerde')
    municipality_key = row.get('gemeindeziffer')            
    wkb_geometry = parse_geometry(row.get('geometrie'))

    sql = '''
    INSERT INTO sh_archaeological_monument (
        object_name, proper_name, object_number, district_name, municipality_name,
        object_description, object_significance, protection_scope, date_registered,
        date_modified, status, heritage_authority, municipality_key, wkb_geometry
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
    '''

    try:
        cur.execute(sql, (object_name, proper_name, object_number, district_name,
            municipality_name, object_description, object_significance, protection_scope,
            date_registered, date_modified, status, heritage_authority, municipality_key,
            wkb_geometry.wkb))

        last_inserted_id = cur.fetchone()[0]

        log.info(f'inserted monument with proper_name {proper_name} with id {last_inserted_id}')
    except Exception as e:
        log.error(e)


def read_json(path):
    try:
        with open(path, 'r') as f:
            json_data = json.loads(f.read())

            return json_data
    except Exception as e:
        log.error(e)


def save_json(absolute_path, data):
    Path(absolute_path).parent.mkdir(parents=True, exist_ok=True)

    with open(absolute_path, 'wb') as f:
        f.write(data)

        log.info(f'saved data to {absolute_path}')


def download_json(url):
    try:
        r = httpx.get(url)
    except ReadTimeout as e:
        time.sleep(5)
        r = download_json(url)
    finally:
        if r.status_code != httpx.codes.OK:
            log.error(f'{url} returned status {r.status_code}')

            return None
        
        log.info(f'downloaded content from {url}')

        return r.content


def extract_filename(url):
    parsed_url = urlparse(url)
    path = parsed_url.path

    filename = os.path.basename(path)

    return filename


def calculate_md5(absolute_path):
    if not absolute_path.exists():
        return None

    md5_hash = hashlib.md5()

    with open(absolute_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()


def calculate_md5_from_data(json_data):
    md5_hash = hashlib.md5()

    if isinstance(json_data, bytes):
        md5_hash.update(json_data)
    else:
        md5_hash.update(json_data.encode('utf-8'))

    return md5_hash.hexdigest()


def save_file_if_different(absolute_path, json_data):
    json_data_md5 = calculate_md5_from_data(json_data)
    existing_md5 = calculate_md5(absolute_path)
    
    if json_data_md5 != existing_md5:
        save_json(absolute_path, json_data)

        return json_data
    else:
        return read_json(absolute_path)


@click.command()
@click.option('--env', '-e', type=str, required=True, help='Path to local dot env file')
@click.option('--url', '-u', type=str, required=True, help='Full source url you want to use')
@click.option('--target', '-t', type=str, required=True, help='Target directory to save download')
@click.option('--verbose', '-v', is_flag=True, help='Print more verbose output')
@click.option('--debug', '-d', is_flag=True, help='Print detailed debug output')
def main(env, url, target, verbose, debug):
    if debug:
        log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)
    if verbose:
        log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)
        log.info(f'set logging level to verbose')
    else:
        log.basicConfig(format='%(levelname)s: %(message)s')

    recursion_limit = sys.getrecursionlimit()
    log.info(f'your system recursion limit: {recursion_limit}')

    conn = connect_database(env)
    json_data = download_json(url)

    if json_data is None:
        sys.exit(1)

    filename = extract_filename(url)
    absolute_path = Path(f'{target}/{filename}').resolve()
    data = save_file_if_different(absolute_path, json_data)
    parse_json(conn, data)


if __name__ == '__main__':
    sys.excepthook = log_exceptions

    main()
