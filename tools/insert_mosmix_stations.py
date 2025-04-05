from decimal import Decimal
import os
import re
import sys
import csv
import click
import traceback
import logging as log
import psycopg2
import psycopg2.extras

from datetime import datetime
from shapely.geometry import Point
from dotenv import load_dotenv
from pathlib import Path


# log uncaught exceptions
def log_exceptions(type, value, tb):
    for line in traceback.TracebackException(type, value, tb).format(chain=True):
        log.exception(line)

    log.exception(value)

    sys.__excepthook__(type, value, tb)  # calls default excepthook


def connect_database(env_path):
    try:
        load_dotenv(dotenv_path=Path(env_path))

        conn = psycopg2.connect(
            database=os.getenv('DB_NAME'),
            password=os.getenv('DB_PASS'),
            user=os.getenv('DB_USER'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )

        conn.autocommit = True

        log.info('connection to database established')

        return conn
    except Exception as e:
        log.error(e)

        sys.exit(1)


def parse_value(value, conversion_func=None):
    try:
        return conversion_func(value) if conversion_func else value
    except ValueError:
        return None


def parse_line(line):
    column_positions = [
        (0, 5),     # ID: 01001
        (6, 10),    # ICAO: ENJA
        (11, 31),   # NAME: JAN MAYEN
        (31, 38),   # LAT: 70.56
        (40, 47),   # LON: -8.40
        (50, 54)    # ELEV: 10
    ]

    return [line[start:end].strip() for start, end in column_positions]


def parse_coords(coord):
    try:
        coord = coord.strip().split('.')
        degrees = int(coord[0])
        minutes = int(coord[1])

        coordinate = round(degrees + (minutes / 60), 6)

        return coordinate
    except Exception as e:
        log.error(e)
        return None


def insert_row(cur, row):
    station_id = parse_value(row[0]).strip()
    icao_code = parse_value(row[1]).strip()
    station_name = parse_value(row[2]).strip()
    latitude = parse_value(parse_coords(row[3]), float)
    longitude = parse_value(parse_coords(row[4]), float)
    station_elevation = parse_value(row[5], int)
    wkb_geometry = None

    if longitude and latitude:
        point = Point(longitude, latitude)
        wkb_geometry = point.wkb

    sql = '''
        INSERT INTO global_mosmix_stations (station_id, icao_code,
            station_name, latitude, longitude, station_elevation, wkb_geometry)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
    '''

    try:
        cur.execute(sql, (
            station_id, icao_code, station_name, latitude, longitude,
            station_elevation, wkb_geometry
        ))

        last_inserted_id = cur.fetchone()[0]

        log.info(f'inserted station {station_name} with id {last_inserted_id}')
    except Exception as e:
        log.error(e)


def read_csv(conn, src):
    cur = conn.cursor()

    with open(src, mode='r', encoding='ISO-8859-1', newline='') as csvfile:
        header = next(csvfile).strip().split()[:-2]
        next(csvfile)
        rows = [parse_line(line) for line in csvfile]      

    for row in rows:
        insert_row(cur, row)


@click.command()
@click.option('--env', '-e', type=str, required=True, help='Path to local dot env file')
@click.option('--src', '-s', type=str, required=True, help='Path to your local file')
@click.option('--verbose', '-v', is_flag=True, help='Print more verbose output')
@click.option('--debug', '-d', is_flag=True, help='Print detailed debug output')
def main(env, src, verbose, debug):
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
    data = read_csv(conn, src)


if __name__ == '__main__':
    sys.excepthook = log_exceptions

    main()
