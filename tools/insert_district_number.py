import os
import re
import sys
import json
import click
import hashlib
import traceback
import logging as log
import psycopg2
import httpx

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


def parse_json(conn, data):
    cur = conn.cursor()

    for row in data['daten']:
        insert_row(cur, row)


def insert_row(cur, row):
    district_number = row[0]
    district_name = row[1]
    notes = row[2]

    sql = '''
        INSERT INTO de_district_numbers (district_number, district_name, notes)
        VALUES (%s, %s, %s) RETURNING id
    '''

    try:
        cur.execute(sql, (district_number, district_name, notes))

        last_inserted_id = cur.fetchone()[0]

        log.info(f'inserted {district_name} with id {last_inserted_id}')
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
