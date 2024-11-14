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


def get_value(element, tag_name, default=None, cast_type=str):
    tag = element.find(tag_name)

    if tag is not None and tag.text:
        try:
            return cast_type(tag.text)
        except ValueError:
            return default

    return default


def insert_row(cur, row):
    official_municipality_key = row['ags']
    municipality_name = row['gemeindename']
    cadastral_district_number = int(row['gemarkungsnummer'])
    cadastral_district_name = row['gemarkungsname']

    sql = '''
        INSERT INTO de_cadastral_district_meta (official_municipality_key,
            municipality_name, cadastral_district_number, cadastral_district_name)
        VALUES (%s, %s, %s, %s) RETURNING id
    '''

    try:
        cur.execute(sql, (official_municipality_key, municipality_name,
            cadastral_district_number, cadastral_district_name))

        last_inserted_id = cur.fetchone()[0]

        log.info(f'inserted {cadastral_district_name} with id {last_inserted_id}')
    except Exception as e:
        log.error(e)


def read_solar_units(conn, src):
    context = etree.iterparse(src, events=('end',), tag='EinheitSolar')
    units = []
    
    for event, elem in context:
        unit = {
            'unit_registration_number': get_value(elem, 'EinheitMastrNummer'),
            'last_update': get_value(elem, 'DatumLetzteAktualisierung'),
            'location_registration_number': get_value(elem, 'LokationMaStRNummer'),
            'network_operator_status': get_value(elem, 'NetzbetreiberpruefungStatus'),
            'operator_registration_number': get_value(elem, 'AnlagenbetreiberMastrNummer'),
            'country': get_value(elem, 'Land'),
            'state': get_value(elem, 'Bundesland'),
            'district': get_value(elem, 'Landkreis'),
            'municipality': get_value(elem, 'Gemeinde'),
            'municipality_key': get_value(elem, 'Gemeindeschluessel'),
            'postcode': get_value(elem, 'Postleitzahl'),
            'city': get_value(elem, 'Ort'),
            'registration_date': get_value(elem, 'Registrierungsdatum'),
            'commissioning_date': get_value(elem, 'Inbetriebnahmedatum'),
            'system_status': get_value(elem, 'EinheitSystemstatus'),
            'operational_status': get_value(elem, 'EinheitBetriebsstatus'),
            'not_present_migrated_units': get_value(elem, 'NichtVorhandenInMigriertenEinheiten'),
            'power_unit_name': get_value(elem, 'NameStromerzeugungseinheit'),
            'weic_nv': get_value(elem, 'Weic_nv'),
            'power_plant_number_nv': get_value(elem, 'Kraftwerksnummer_nv'),
            'energy_source': get_value(elem, 'Energietraeger'),
            'gross_power': get_value(elem, 'Bruttoleistung'),
            'net_rated_power': get_value(elem, 'Nettonennleistung'),
            'remote_controllability': get_value(elem, 'FernsteuerbarkeitNb'),
            'type_feed_in': get_value(elem, 'Einspeisungsart'),
            'assigned_active_power_inverter': get_value(elem, 'ZugeordneteWirkleistungWechselrichter'),
            'amount_modules': get_value(elem, 'AnzahlModule'),
            'location': get_value(elem, 'Lage'),
            'power_limitation': get_value(elem, 'Leistungsbegrenzung'),
            'uniform_orientation_tilt_angle': get_value(elem, 'EinheitlicheAusrichtungUndNeigungswinkel'),
            'main_orientation': get_value(elem, 'Hauptausrichtung'),
            'main_orientation_tilt_angle': get_value(elem, 'HauptausrichtungNeigungswinkel'),
            'usage_area': get_value(elem, 'Nutzungsbereich'),
            'eeg_registration_number': get_value(elem, 'EegMaStRNummer')
        }

        units.append(unit)
        print(unit)
        elem.clear()

        while elem.getprevious() is not None:
            del elem.getparent()[0]

    return units


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
    data = read_solar_units(conn, Path(src))


if __name__ == '__main__':
    sys.excepthook = log_exceptions

    main()
