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
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


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
        'network_operator_audit', 'operator_registration_number', 'country', 'state',
        'district', 'municipality_name', 'municipality_key', 'postcode', 'city',
        'registration_date', 'commissioning_date', 'system_status', 'unit_operational_status',
        'not_present_migrated_units', 'power_unit_name', 'weic_not_available',
        'power_plant_number_not_available', 'energy_source', 'gross_power', 'net_rated_power',
        'remote_controllability', 'supply_type', 'assigned_active_power_inverter',
        'amount_modules', 'location', 'power_limitation', 'uniform_orientation_tilt_angle',
        'main_orientation', 'main_orientation_tilt_angle', 'usage_area', 'eeg_registration_number'
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
            'network_operator_audit': parse_value(elem, 'NetzbetreiberpruefungStatus'),
            'operator_registration_number': parse_value(elem, 'AnlagenbetreiberMastrNummer'),
            'country': parse_value(elem, 'Land'),
            'state': parse_value(elem, 'Bundesland'),
            'district': parse_value(elem, 'Landkreis'),
            'municipality_name': parse_value(elem, 'Gemeinde'),
            'municipality_key': parse_value(elem, 'Gemeindeschluessel'),
            'postcode': parse_value(elem, 'Postleitzahl'),
            'city': parse_value(elem, 'Ort'),
            'registration_date': parse_value(elem, 'Registrierungsdatum', parse_datetime),
            'commissioning_date': parse_value(elem, 'Inbetriebnahmedatum', parse_datetime),
            'system_status': parse_value(elem, 'EinheitSystemstatus'),
            'unit_operational_status': parse_value(elem, 'EinheitBetriebsstatus'),
            'not_present_migrated_units': parse_value(elem, 'NichtVorhandenInMigriertenEinheiten'),
            'power_unit_name': parse_value(elem, 'NameStromerzeugungseinheit'),
            'weic_not_available': parse_value(elem, 'Weic_nv'),
            'power_plant_number_not_available': parse_value(elem, 'Kraftwerksnummer_nv'),
            'energy_source': parse_value(elem, 'Energietraeger'),
            'gross_power': parse_value(elem, 'Bruttoleistung'),
            'net_rated_power': parse_value(elem, 'Nettonennleistung'),
            'remote_controllability': parse_value(elem, 'FernsteuerbarkeitNb'),
            'supply_type': parse_value(elem, 'Einspeisungsart'),
            'assigned_active_power_inverter': parse_value(elem, 'ZugeordneteWirkleistungWechselrichter'),
            'amount_modules': parse_value(elem, 'AnzahlModule'),
            'location': parse_value(elem, 'Lage'),
            'power_limitation': parse_value(elem, 'Leistungsbegrenzung'),
            'uniform_orientation_tilt_angle': parse_value(elem, 'EinheitlicheAusrichtungUndNeigungswinkel'),
            'main_orientation': parse_value(elem, 'Hauptausrichtung'),
            'main_orientation_tilt_angle': parse_value(elem, 'HauptausrichtungNeigungswinkel'),
            'usage_area': parse_value(elem, 'Nutzungsbereich'),
            'eeg_registration_number': parse_value(elem, 'EegMaStRNummer')
        }

        insert_row(cur, unit)
        elem.clear()

        while elem.getprevious() is not None:
            del elem.getparent()[0]


@click.command()
@click.option('--env', '-e', type=str, required=True, help='Set your local dot env path')
@click.option('--src', '-s', type=click.Path(exists=True), required=True, help='Set src path to your csv')
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
