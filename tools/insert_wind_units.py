import os
import sys
import click
import traceback
import logging as log
import psycopg2
import psycopg2.extras

from datetime import datetime
from shapely.geometry import Point
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
        'network_operator_audit_id', 'operator_registration_number', 'country_id', 'state_id',
        'district', 'municipality_name', 'municipality_key', 'postcode', 'cadastral_district',
        'field_parcel_numbers', 'street_not_found', 'house_number_not_available',
        'house_number_not_found', 'city', 'longitude', 'latitude', 'registration_date',
        'commissioning_date', 'unit_system_status_id', 'unit_operational_status',
        'not_present_migrated_units', 'power_unit_name', 'weic_not_available',
        'power_plant_number_not_available', 'energy_source_id', 'gross_power',
        'net_rated_power', 'connection_high_voltage', 'remote_control_capability_nb',
        'remote_control_capability_dv', 'supply_type_id', 'gen_registration_number',
        'wind_park_name', 'location_id', 'manufacturer_id', 'technology_id', 'model_designation',
        'hub_height', 'rotor_diameter', 'rotor_blade_deicing_system',
        'shutdown_power_limitation', 'eeg_registration_number', 'wkb_geometry'
    ]

    sql = f'''
        INSERT INTO de_wind_units ({", ".join(columns)})
        VALUES ({", ".join(["%s"] * len(columns))}) RETURNING id
    '''

    try:
        cur.execute(sql, [row.get(col) for col in columns])
        last_inserted_id = cur.fetchone()[0]
        unit_id = row['unit_registration_number']

        log.info(f'Inserted {unit_id} with ID {last_inserted_id}')
    except Exception as e:
        log.error(f'Error inserting row: {e}')


def read_wind_units(conn, src):
    cur = conn.cursor()

    context = etree.iterparse(src, events=('end',), tag='EinheitWind')

    for event, elem in context:
        unit = {
            'unit_registration_number': parse_value(elem, 'EinheitMastrNummer'),
            'last_update': parse_value(elem, 'DatumLetzteAktualisierung'),
            'location_registration_number': parse_value(elem, 'LokationMaStRNummer'),
            'network_operator_audit_id': parse_value(elem, 'NetzbetreiberpruefungStatus'),
            'operator_registration_number': parse_value(elem, 'AnlagenbetreiberMastrNummer'),
            'country_id': parse_value(elem, 'Land'),
            'state_id': parse_value(elem, 'Bundesland'),
            'district': parse_value(elem, 'Landkreis'),
            'municipality_name': parse_value(elem, 'Gemeinde'),
            'municipality_key': parse_value(elem, 'Gemeindeschluessel'),
            'postcode': parse_value(elem, 'Postleitzahl'),
            'cadastral_district': parse_value(elem, 'Gemarkung'),
            'field_parcel_numbers': parse_value(elem, 'FlurFlurstuecknummern'),
            'street_not_found': parse_value(elem, 'StrasseNichtGefunden'),
            'house_number_not_available': parse_value(elem, 'Hausnummer_nv'),
            'house_number_not_found': parse_value(elem, 'HausnummerNichtGefunden'),
            'city': parse_value(elem, 'Ort'),
            'longitude': parse_value(elem, 'Laengengrad', float),
            'latitude': parse_value(elem, 'Breitengrad', float),
            'registration_date': parse_value(elem, 'Registrierungsdatum', parse_datetime),
            'commissioning_date': parse_value(elem, 'Inbetriebnahmedatum', parse_datetime),
            'unit_system_status': parse_value(elem, 'EinheitSystemstatus'),
            'unit_operational_status': parse_value(elem, 'EinheitBetriebsstatus'),
            'not_present_migrated_units': parse_value(elem, 'NichtVorhandenInMigriertenEinheiten'),
            'power_unit_name': parse_value(elem, 'NameStromerzeugungseinheit'),
            'weic_not_available': parse_value(elem, 'Weic_nv'),
            'power_plant_number_not_available': parse_value(elem, 'Kraftwerksnummer_nv'),
            'energy_source_id': parse_value(elem, 'Energietraeger'),
            'gross_power': parse_value(elem, 'Bruttoleistung'),
            'net_rated_power': parse_value(elem, 'Nettonennleistung'),
            'connection_high_voltage': parse_value(elem, 'AnschlussAnHoechstOderHochSpannung'),
            'remote_control_capability_nb': parse_value(elem, 'FernsteuerbarkeitNb'),
            'remote_control_capability_dv': parse_value(elem, 'FernsteuerbarkeitDv'),
            'supply_type_id': parse_value(elem, 'Einspeisungsart'),
            'gen_registration_number': parse_value(elem, 'GenMastrNummer'),
            'wind_park_name': parse_value(elem, 'NameWindpark'),
            'location_id': parse_value(elem, 'Lage'),
            'manufacturer': parse_value(elem, 'Hersteller'),
            'technology': parse_value(elem, 'Technologie'),
            'model_designation': parse_value(elem, 'Typenbezeichnung'),
            'hub_height': parse_value(elem, 'Nabenhoehe'),
            'rotor_diameter': parse_value(elem, 'Rotordurchmesser'),
            'rotor_blade_deicing_system': parse_value(elem, 'Rotorblattenteisungssystem'),
            'shutdown_power_limitation': parse_value(elem, 'AuflageAbschaltungLeistungsbegrenzung'),
            'eeg_registration_number': parse_value(elem, 'EegMaStRNummer'),
            'wkb_geometry': None
        }

        if unit['longitude'] and unit['latitude']:
            point = Point(unit['longitude'], unit['latitude'])
            unit['wkb_geometry'] = point.wkb

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
    read_wind_units(conn, Path(src))


if __name__ == '__main__':
    sys.excepthook = log_exceptions

    main()
