import os
import sys
import click
import traceback
import logging as log
import psycopg2

from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from lxml import etree



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


def parse_datetime(s):
    date_string = s 

    if '.' in date_string:
        parts = date_string.split('.')
        date_string = f'{parts[0]}.{parts[1][:6]}'

    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f')


def parse_date(s):
    return datetime.strptime(s, '%Y-%m-%d')


def parse_value(elem, tag_name, conversion_func=None):
    tag = elem.find(tag_name)

    if tag is None or not tag.text:
        return None

    try:
        return conversion_func(tag.text) if conversion_func else tag.text
    except ValueError:
        return None


def insert_row(cur, row):
    columns = [
        'unit_registration_number', 'last_update', 'location_registration_number',
        'network_operator_audit_id', 'operator_registration_number', 'country_id', 'state_id',
        'district', 'municipality_name', 'municipality_key', 'postcode', 'city',
        'registration_date', 'commissioning_date', 'unit_system_status_id', 'unit_operational_status_id',
        'not_present_migrated_units', 'unit_name', 'weic_not_available',
        'power_plant_number_not_available', 'energy_source_id', 'gross_capacity', 'net_nominal_capacity',
        'remote_controllability', 'supply_type_id', 'assigned_active_power_inverter',
        'amount_modules', 'location_id', 'power_limitation_id', 'uniform_orientation_tilt_angle_id',
        'main_orientation_id', 'main_orientation_tilt_angle_id', 'usage_area_id', 'eeg_registration_number'
    ]

    sql = f'''
        INSERT INTO de_solar_units ({", ".join(columns)})
        VALUES ({", ".join(["%s"] * len(columns))}) RETURNING id
    '''

    try:
        cur.execute(sql, [row.get(col) for col in columns])
        last_inserted_id = cur.fetchone()[0]
        unit_id = row['unit_registration_number']

        log.info(f'Inserted {unit_id} with ID {last_inserted_id}')
    except Exception as e:
        log.error(f'Error inserting row: {e}')


def read_solar_units(conn, src):
    cur = conn.cursor()

    context = etree.iterparse(src, events=('end',), tag='EinheitSolar')

    for event, elem in context:
        unit = {
            'unit_registration_number': parse_value(elem, 'EinheitMastrNummer'),
            'last_update': parse_value(elem, 'DatumLetzteAktualisierung', parse_datetime),
            'location_registration_number': parse_value(elem, 'LokationMaStRNummer'),
            'network_operator_audit_id': parse_value(elem, 'NetzbetreiberpruefungStatus'),
            'operator_registration_number': parse_value(elem, 'AnlagenbetreiberMastrNummer'),
            'country_id': parse_value(elem, 'Land', int),
            'state_id': parse_value(elem, 'Bundesland', int),
            'district': parse_value(elem, 'Landkreis'),
            'municipality_name': parse_value(elem, 'Gemeinde'),
            'municipality_key': parse_value(elem, 'Gemeindeschluessel'),
            'postcode': parse_value(elem, 'Postleitzahl'),
            'city': parse_value(elem, 'Ort'),
            'registration_date': parse_value(elem, 'Registrierungsdatum', parse_date),
            'commissioning_date': parse_value(elem, 'Inbetriebnahmedatum', parse_date),
            'unit_system_status_id': parse_value(elem, 'EinheitSystemstatus', int),
            'unit_operational_status_id': parse_value(elem, 'EinheitBetriebsstatus', int),
            'not_present_migrated_units': parse_value(elem, 'NichtVorhandenInMigriertenEinheiten'),
            'unit_name': parse_value(elem, 'NameStromerzeugungseinheit'),
            'weic_not_available': parse_value(elem, 'Weic_nv'),
            'power_plant_number_not_available': parse_value(elem, 'Kraftwerksnummer_nv'),
            'energy_source_id': parse_value(elem, 'Energietraeger', int),
            'gross_capacity': parse_value(elem, 'Bruttoleistung', float),
            'net_nominal_capacity': parse_value(elem, 'Nettonennleistung'),
            'remote_controllability': parse_value(elem, 'FernsteuerbarkeitNb'),
            'supply_type_id': parse_value(elem, 'Einspeisungsart', int),
            'assigned_active_power_inverter': parse_value(elem, 'ZugeordneteWirkleistungWechselrichter'),
            'amount_modules': parse_value(elem, 'AnzahlModule'),
            'location_id': parse_value(elem, 'Lage', int),
            'power_limitation_id': parse_value(elem, 'Leistungsbegrenzung', int),
            'uniform_orientation_tilt_angle_id': parse_value(elem, 'EinheitlicheAusrichtungUndNeigungswinkel'),
            'main_orientation_id': parse_value(elem, 'Hauptausrichtung', int),
            'main_orientation_tilt_angle_id': parse_value(elem, 'HauptausrichtungNeigungswinkel', int),
            'usage_area_id': parse_value(elem, 'Nutzungsbereich', int),
            'eeg_registration_number': parse_value(elem, 'EegMaStRNummer')
        }

        insert_row(cur, unit)
        elem.clear()

        while elem.getprevious() is not None:
            del elem.getparent()[0]


@click.command()
@click.option('--env', '-e', type=str, required=True, help='Set your local dot env path')
@click.option('--src', '-s', type=click.Path(exists=True), required=True, help='Set src path to your xml')
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
    read_solar_units(conn, Path(src))


if __name__ == '__main__':
    sys.excepthook = log_exceptions

    main()
