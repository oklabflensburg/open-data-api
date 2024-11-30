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
    date_string = s 

    if '.' in date_string:
        parts = date_string.split('.')
        date_string = f'{parts[0]}.{parts[1][:6]}'

    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f')


def parse_date(s):
    return datetime.strptime(s, '%Y-%m-%d')


def parse_bool(v):
    return v.lower() in ('yes', 'true', 't', '1')


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
        'network_operator_audit_id', 'operator_registration_number', 'country_id',
        'state_id', 'district', 'municipality_name', 'municipality_key',
        'postcode', 'city', 'citizen_energy', 'network_operator_inspection_date',
        'final_decommissioning_date', 'temporary_decommissioning_date',
        'operation_resumption_date', 'planned_commissioning_date',
        'legacy_system_registration_number', 'former_operator_registration_number',
        'actual_operator_change_date', 'operator_change_registration_date',
        'w_code', 'w_code_display_name', 'power_plant_number', 'high_voltage_connection',
        'remote_control_direct_marketer', 'cadastral_district', 'plots_or_parcel_numbers',
        'street', 'street_not_found', 'housenumber', 'housenumber_not_found',
        'address_addition', 'longitude', 'latitude', 'utm_zone', 'utm_east', 'utm_north',
        'gauss_kruger_north', 'gauss_kruger_east', 'black_start_capability',
        'island_operation_capability', 'responsible_partner_number', 'registration_date',
        'commissioning_date', 'unit_system_status_id', 'unit_operational_status_id',
        'not_present_migrated_units', 'unit_name', 'weic_not_available',
        'power_plant_number_not_available', 'energy_source_id', 'gross_capacity',
        'net_nominal_capacity', 'remote_controllability', 'supply_type_id',
        'assigned_active_power_inverter', 'amount_modules', 'location_id',
        'power_limitation_id', 'uniform_orientation_tilt_angle', 'main_orientation_id',
        'main_orientation_tilt_angle_id', 'usage_area_id', 'eeg_registration_number',
        'wkb_geometry'
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
            # MaStR-Nummer der Einheit
            'unit_registration_number': parse_value(elem, 'EinheitMastrNummer'),

            # Datum der letzten Aktualisierung an diesem Objekt
            'last_update': parse_value(elem, 'DatumLetzteAktualisierung', parse_datetime),

            # MaStR-Nummer der Lokation
            'location_registration_number': parse_value(elem, 'LokationMaStRNummer'),

            # Der Status der letzten Netzbetreiberprüfung, insofern eine durchgeführt wurde
            'network_operator_audit_id': parse_value(elem, 'NetzbetreiberpruefungStatus'),

            # MaStR-Nummer des Betreibers der Einheit
            'operator_registration_number': parse_value(elem, 'AnlagenbetreiberMastrNummer'),

            # Standort der Einheit: Land
            'country_id': parse_value(elem, 'Land', int),

            # Standort der Einheit: Bundesland
            'state_id': parse_value(elem, 'Bundesland', int),

            # Standort der Einheit: Landkreis
            'district': parse_value(elem, 'Landkreis'),

            # Standort der Einheit: Gemeinde
            'municipality_name': parse_value(elem, 'Gemeinde'),

            # Standort der Einheit: Gemeindeschlüssel
            'municipality_key': parse_value(elem, 'Gemeindeschluessel'),

            # Standort der Einheit: Postleitzahl
            'postcode': parse_value(elem, 'Postleitzahl'),

            # Standort der Einheit: Ort
            'city': parse_value(elem, 'Ort'),

            # Bürgerenergieeigenschaft der Einheit
            'citizen_energy': parse_value(elem, 'Buergerenergie'),

            # Datum der letzten Netzbetreiberprüfung, insofern eine durchgeführt wurde
            'network_operator_inspection_date': parse_value(elem, 'NetzbetreiberpruefungDatum', parse_date),

            # Datum der endgültigen Stilllegung der Einheit
            'final_decommissioning_date': parse_value(elem, 'DatumEndgueltigeStilllegung', parse_date),

            # Beginn der vorläufigen Stilllegung der Einheit
            'temporary_decommissioning_date': parse_value(elem, 'DatumBeginnVoruebergehendeStilllegung', parse_date),

            # Datum der Wiederaufnahme des Betriebs
            'operation_resumption_date': parse_value(elem, 'DatumWiederaufnahmeBetrieb', parse_date),

            # Geplantes Inbetriebnahmedatum der Stromerzeugungsseinheit
            'planned_commissioning_date': parse_value(elem, 'GeplantesInbetriebnahmedatum', parse_date),

            # Angaben über optional vorhandene MaStR-Nummer aus der Bestandsanlagenverwaltung
            'legacy_system_registration_number': parse_value(elem, 'BestandsanlageMastrNummer'),

            # MaStR-Nummer des ehemaligen Betreibers der Einheit
            'former_operator_registration_number': parse_value(elem, 'AltAnlagenbetreiberMastrNummer'),

            # Datum des realen Betreiberwechsels
            'actual_operator_change_date': parse_value(elem, 'DatumDesBetreiberwechsels', parse_date),

            # Datum der Registrierung des Betreiberwechsels
            'operator_change_registration_date': parse_value(elem, 'DatumRegistrierungDesBetreiberwechsels', parse_date),

            # W-Code der Stromerzeugungseinheit
            'w_code': parse_value(elem, 'Weic'),

            # Displayname des W-EIC
            'w_code_display_name': parse_value(elem, 'WeicDisplayName'),

            # Bundesnetzagentur-Kraftwerksnummer
            'power_plant_number': parse_value(elem, 'Kraftwerksnummer'),

            # Die Stromerzeugungseinheit ist an ein Höchst- oder Hochspannungsnetz angeschlossen
            'high_voltage_connection': parse_value(elem, 'AnschlussAnHoechstOderHochSpannung'),

            # Fernsteuerbarkeit der Einheit durch einen Direktvermarkter
            'remote_control_direct_marketer': parse_value(elem, 'FernsteuerbarkeitDv', parse_bool),

            # Standort der Einheit: Gemarkung
            'cadastral_district': parse_value(elem, 'Gemarkung'),

            # Standort der Einheit: Flur und/oder Flurstücke
            'plots_or_parcel_numbers': parse_value(elem, 'FlurFlurstuecknummern'),

            # Standort der Einheit: Straße
            'street': parse_value(elem, 'Straße'),

            # Angabe, dass die angegebene Strasse nicht aus dem BKG-Adressdatenbestand stammt
            'street_not_found': parse_value(elem, 'StrasseNichtGefunden', parse_bool),

            # Standort der Einheit: Hausnummer
            'housenumber': parse_value(elem, 'Hausnummer'),

            # Angabe, dass die angegebene Hausnummer nicht aus dem BKG-Adressdatenbestand stammt
            'housenumber_not_found': parse_value(elem, 'HausnummerNichtGefunden', parse_bool),

            # Standort der Einheit: Adresszusatz
            'address_addition': parse_value(elem, 'Adresszusatz'),

            # Koordinaten der Einheit: Längengrad
            'longitude': parse_value(elem, 'Laengengrad', float),

            # Koordinaten der Einheit: Breitengrad
            'latitude': parse_value(elem, 'Breitengrad', float),

            # Koordinaten der Einheit: UTM-Zonenwert
            'utm_zone': parse_value(elem, 'UtmZonenwert', int),

            # Koordinaten der Einheit: UTM-Ost
            'utm_east': parse_value(elem, 'UtmEast', float),

            # Koordinaten der Einheit: UTM-Nord
            'utm_north': parse_value(elem, 'UtmNorth', float),

            # Koordinaten der Einheit: Gauß-Krüger-Hochwert
            'gauss_kruger_north': parse_value(elem, 'GaussKruegerHoch', float),

            # Koordinaten der Einheit: Gauß-Krüger-Rechtswert
            'gauss_kruger_east': parse_value(elem, 'GaussKruegerRechts', float),

            # Schwarzstartfähigkeit der Einheit
            'black_start_capability': parse_value(elem, 'Schwarzstartfaehigkeit', parse_bool),

            # Inselbetriebsfähigkeit der Einheit
            'island_operation_capability': parse_value(elem, 'Inselbetriebsfaehigkeit', parse_bool),

            # Marktpartner-ID des Einsatzverantwortlichen
            'responsible_partner_number': parse_value(elem, 'Einsatzverantwortlicher'),

            # Registrierungsdatum der Einheit
            'registration_date': parse_value(elem, 'Registrierungsdatum', parse_date),

            # Datum der Inbetriebnahme
            'commissioning_date': parse_value(elem, 'Inbetriebnahmedatum', parse_date),

            # Systemstatus der Einheit
            'unit_system_status_id': parse_value(elem, 'EinheitSystemstatus', int),

            # Betriebsstatus der Einheit
            'unit_operational_status_id': parse_value(elem, 'EinheitBetriebsstatus', int),

            # Angabe über das Nichtvorhandensein in den migrierten Einheiten
            'not_present_migrated_units': parse_value(elem, 'NichtVorhandenInMigriertenEinheiten', parse_bool),

            # Vom Betreiber frei wählbare Bezeichnung der Stromerzeugungseinheit
            'unit_name': parse_value(elem, 'NameStromerzeugungseinheit'),

            'weic_not_available': parse_value(elem, 'Weic_nv', parse_bool),

            'power_plant_number_not_available': parse_value(elem, 'Kraftwerksnummer_nv', parse_bool),

            # Energieträger der Einheit
            'energy_source_id': parse_value(elem, 'Energietraeger', int),

            # Bruttoleistung in kW
            'gross_capacity': parse_value(elem, 'Bruttoleistung', float),

            # Nettonennleistung in kW
            'net_nominal_capacity': parse_value(elem, 'Nettonennleistung', float),

            # Fernsteuerbarkeit der Einheit durch einen Netzbetreiber
            'remote_controllability': parse_value(elem, 'FernsteuerbarkeitNb', parse_bool),

            # Volleinspeisung oder TeileinspeisungEigenverbrauch
            'supply_type_id': parse_value(elem, 'Einspeisungsart', int),

            # Wechselrichterleistung der Stromerzeugungseinheit
            'assigned_active_power_inverter': parse_value(elem, 'ZugeordneteWirkleistungWechselrichter', float),

            # Anzahl der Module dieser Stromerzeugungseinheit
            'amount_modules': parse_value(elem, 'AnzahlModule', int),

            # Errichtungsort der Stromerzeugungseinheit
            'location_id': parse_value(elem, 'Lage', int),

            # Die Leistung der Stromerzeugungseinheit ist auf einen bestimmten prozentualen Leistungsanteil begrenzt
            'power_limitation_id': parse_value(elem, 'Leistungsbegrenzung', int),

            # Angabe, ob einheitliche Ausrichtung und Neigungswinkel bestehen
            'uniform_orientation_tilt_angle': parse_value(elem, 'EinheitlicheAusrichtungUndNeigungswinkel', parse_bool),

            # Die Ausrichtung bezeichnet die Himmelsrichtung
            'main_orientation_id': parse_value(elem, 'Hauptausrichtung', int),

            # Der Neigungswinkel bezeichnet den Winkel gegenüber der Horizontalen
            'main_orientation_tilt_angle_id': parse_value(elem, 'HauptausrichtungNeigungswinkel', int),

            # Vorrangige Nutzung des in Anspruch genommenen Gebäudes
            'usage_area_id': parse_value(elem, 'Nutzungsbereich', int),

            # MaStR-Nummer der EEG-Anlage
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
