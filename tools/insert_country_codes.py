import os
import sys
import csv
import click
import traceback
import logging as log
import psycopg2

from datetime import datetime
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


def parse_date(s):
    return datetime.strptime(s, '%Y%m%d')


def parse_value(value, conversion_func=None):
    try:
        return conversion_func(value) if conversion_func else value
    except ValueError:
        return None


def insert_row(cur, row):
    iso_code = parse_value(row['iso_code'])
    numeric_code = parse_value(row['numeric_code'])
    iso_3166_alpha2 = parse_value(row['iso_3166_alpha2'])
    iso_3166_alpha3 = parse_value(row['iso_3166_alpha3'])
    iso_3166_numeric = parse_value(row['iso_3166_numeric'])
    state_abbreviation = parse_value(row['state_abbreviation'])
    state_name = parse_value(row['state_name'])

    sql = '''
        INSERT INTO eu_country_codes (numeric_code, iso_code,
            state_abbreviation, iso_3166_alpha2, iso_3166_alpha3, 
            iso_3166_numeric, state_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
    '''

    try:
        cur.execute(sql, (numeric_code, iso_code, state_abbreviation,
            iso_3166_alpha2, iso_3166_alpha3, iso_3166_numeric, state_name))

        last_inserted_id = cur.fetchone()[0]

        log.info(f'inserted state name {state_name} with id {last_inserted_id}')
    except Exception as e:
        log.error(e)


def read_csv(conn, src):
    cur = conn.cursor()

    with open(src, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
    
        for row in reader:
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
    read_csv(conn, src)


if __name__ == '__main__':
    sys.excepthook = log_exceptions

    main()
