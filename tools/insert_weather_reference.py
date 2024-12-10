#!./venv/bin/python

import os
import sys
import click
import httpx
import traceback
import logging as log
import psycopg2
import psycopg2.extras

from datetime import datetime
from shapely.geometry import Point
from dotenv import load_dotenv
from pathlib import Path
from lxml import html


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


def parse_date(s):
    return datetime.strptime(s, '%d.%m.%Y')


def parse_value(value, conversion_func=None):
    try:
        return conversion_func(value.strip()) if conversion_func else value.strip()
    except ValueError:
        return None


def insert_row(cur, row):
    station_name = parse_value(row[0])
    station_id = parse_value(row[1])
    identifier = parse_value(row[2])
    station_code = parse_value(row[3])
    station_latitude = parse_value(row[4], float)
    station_longitude = parse_value(row[5], float)
    station_elevation = parse_value(row[6], int)
    river_basin_id = parse_value(row[7], int)
    state_name = parse_value(row[8])
    recording_start = parse_value(row[9], parse_date)
    recording_end = parse_value(row[10], parse_date)
    wkb_geometry = None

    # Ensure identifier is padded to 5 digits
    station_id = station_id.zfill(5)

    if station_longitude and station_latitude:
        point = Point(station_longitude, station_latitude)
        wkb_geometry = point.wkb

    sql = '''
        INSERT INTO dwd_station_reference (station_name, station_id, identifier,
            station_code, station_latitude, station_longitude, station_elevation,
            river_basin_id, state_name, recording_start, recording_end, wkb_geometry)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
    '''

    try:
        cur.execute(sql, (station_name, station_id, identifier, station_code,
            station_latitude, station_longitude, station_elevation, river_basin_id,
            state_name, recording_start, recording_end, wkb_geometry))

        last_inserted_id = cur.fetchone()[0]

        log.info(f'inserted station name {station_name} with id {last_inserted_id}')
    except Exception as e:
        log.error(e)


def request_content(url):
    try:
        r = httpx.get(url, timeout=2)

        if r.status_code != 200:
            return None

        content = r.content.decode('ISO-8859-1')

        return content

    except httpx.RequestError as e:
        log.error(e)

        return None


def parse_result(conn, content):
    cur = conn.cursor()

    doc = html.document_fromstring(content)

    rows = doc.xpath('//table/tr')
    # rows = rows[2:]

    for idx, row in enumerate(rows):
        if idx in [0, 1]:
            continue

        row_list = row.xpath('./td/text()')
        insert_row(cur, row_list)


@click.command()
@click.option('--env', '-e', type=str, required=True, help='Set your local dot env path')
@click.option('--url', '-u', type=str, required=True, help='Set url you wish to download')
@click.option('--verbose', '-v', is_flag=True, help='Print more verbose output')
@click.option('--debug', '-d', is_flag=True, help='Print detailed debug output')
def main(env, url, verbose, debug):
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
    content = request_content(url)
    parse_result(conn, content)


if __name__ == '__main__':
    sys.excepthook = log_exceptions

    main()
