-- TABELLE SOLAR EINHEITEN DEUTSCHLAND
DROP TABLE IF EXISTS de_solar_units CASCADE;

CREATE TABLE IF NOT EXISTS de_solar_units (
    id SERIAL PRIMARY KEY,

    -- MaStR-Nummer der Einheit
    unit_registration_number VARCHAR,

    -- Datum der letzten Aktualisierung an diesem Objekt
    last_update TIMESTAMP,

    -- MaStR-Nummer der Lokation
    location_registration_number VARCHAR,

    -- Der Status der letzten Netzbetreiberprüfung, insofern eine durchgeführt wurde
    network_operator_audit_id INT,

    -- MaStR-Nummer des Betreibers der Einheit
    operator_registration_number VARCHAR,

    -- Standort der Einheit: Land
    country_id INT,

    -- Standort der Einheit: Bundesland
    state_id INT,

    -- Standort der Einheit: Landkreis
    district VARCHAR,

    -- Standort der Einheit: Gemeinde
    municipality_name VARCHAR,

    -- Standort der Einheit: Gemeindeschlüssel
    municipality_key VARCHAR,

    -- Standort der Einheit: Postleitzahl
    postcode VARCHAR,

    -- Standort der Einheit: Ort
    city VARCHAR,

    -- Bürgerenergieeigenschaft der Einheit
    citizen_energy BOOLEAN,

    -- Datum der letzten Netzbetreiberprüfung, insofern eine durchgeführt wurde
    network_operator_inspection_date TIMESTAMP,

    -- Datum der endgültigen Stilllegung der Einheit
    final_decommissioning_date TIMESTAMP,

    -- Beginn der vorläufigen Stilllegung der Einheit
    temporary_decommissioning_date TIMESTAMP,

    -- Datum der Wiederaufnahme des Betriebs
    operation_resumption_date TIMESTAMP,

    -- Geplantes Inbetriebnahmedatum der Stromerzeugungsseinheit
    planned_commissioning_date TIMESTAMP,

    -- Angaben über optional vorhandene MaStR-Nummer aus der Bestandsanlagenverwaltung
    legacy_system_registration_number VARCHAR,

    -- MaStR-Nummer des ehemaligen Betreibers der Einheit
    former_operator_registration_number VARCHAR,

    -- Datum des realen Betreiberwechsels
    actual_operator_change_date TIMESTAMP,

    -- Datum der Registrierung des Betreiberwechsels
    operator_change_registration_date TIMESTAMP,

    -- W-Code der Stromerzeugungseinheit
    w_code VARCHAR,

    -- Displayname des W-EIC
    w_code_display_name VARCHAR,

    -- Bundesnetzagentur-Kraftwerksnummer
    power_plant_number VARCHAR,

    -- Die Stromerzeugungseinheit ist an ein Höchst- oder Hochspannungsnetz angeschlossen
    high_voltage_connection VARCHAR,

    -- Fernsteuerbarkeit der Einheit durch einen Direktvermarkter
    remote_control_direct_marketer VARCHAR,

    -- Standort der Einheit: Gemarkung
    cadastral_district VARCHAR,

    -- Standort der Einheit: Flur und/oder Flurstücke
    plots_or_parcel_numbers VARCHAR,

    -- Standort der Einheit: Straße
    street VARCHAR,

    -- Angabe, dass die angegebene Strasse nicht aus dem BKG-Adressdatenbestand stammt
    street_not_found VARCHAR,

    -- Standort der Einheit: Hausnummer
    housenumber VARCHAR,

    -- Angabe, dass die angegebene Hausnummer nicht aus dem BKG-Adressdatenbestand stammt
    housenumber_not_found VARCHAR,

    -- Standort der Einheit: Adresszusatz
    address_addition VARCHAR,

    -- Koordinaten der Einheit: Längengrad
    longitude NUMERIC,

    -- Koordinaten der Einheit: Breitengrad
    latitude NUMERIC,

    -- Koordinaten der Einheit: UTM-Zonenwert
    utm_zone INT,

    -- Koordinaten der Einheit: UTM-Ost
    utm_east NUMERIC,

    -- Koordinaten der Einheit: UTM-Nord
    utm_north NUMERIC,

    -- Koordinaten der Einheit: Gauß-Krüger-Hochwert
    gauss_kruger_north NUMERIC,

    -- Koordinaten der Einheit: Gauß-Krüger-Rechtswert
    gauss_kruger_east NUMERIC,

    -- Schwarzstartfähigkeit der Einheit
    black_start_capability BOOLEAN,

    -- Inselbetriebsfähigkeit der Einheit
    island_operation_capability BOOLEAN,

    -- Marktpartner-ID des Einsatzverantwortlichen
    responsible_partner_number VARCHAR,

    -- Registrierungsdatum der Einheit
    registration_date TIMESTAMP,

    -- Datum der Inbetriebnahme
    commissioning_date TIMESTAMP,

    -- Systemstatus der Einheit
    unit_system_status_id INT,

    -- Betriebsstatus der Einheit
    unit_operational_status_id INT,

    -- Angabe über das Nichtvorhandensein in den migrierten Einheiten
    not_present_migrated_units BOOLEAN,

    -- Vom Betreiber frei wählbare Bezeichnung der Stromerzeugungseinheit
    unit_name VARCHAR,

    weic_not_available BOOLEAN,

    power_plant_number_not_available BOOLEAN,

    -- Energieträger der Einheit
    energy_source_id INT,

    -- Bruttoleistung in kW
    gross_capacity NUMERIC,

    -- Nettonennleistung in kW
    net_nominal_capacity NUMERIC,

    -- Fernsteuerbarkeit der Einheit durch einen Netzbetreiber
    remote_controllability BOOLEAN,

    -- Volleinspeisung oder TeileinspeisungEigenverbrauch
    supply_type_id INT,

    -- Wechselrichterleistung der Stromerzeugungseinheit
    assigned_active_power_inverter NUMERIC,

    -- Anzahl der Module dieser Stromerzeugungseinheit
    amount_modules INT,

    -- Errichtungsort der Stromerzeugungseinheit
    location_id INT,

    -- Die Leistung der Stromerzeugungseinheit ist auf einen bestimmten prozentualen Leistungsanteil begrenzt
    power_limitation_id INT,

    -- Angabe, ob einheitliche Ausrichtung und Neigungswinkel bestehen
    uniform_orientation_tilt_angle BOOLEAN,

    -- Die Ausrichtung bezeichnet die Himmelsrichtung
    main_orientation_id INT,

    -- Der Neigungswinkel bezeichnet den Winkel gegenüber der Horizontalen
    main_orientation_tilt_angle_id INT,

    -- Vorrangige Nutzung des in Anspruch genommenen Gebäudes
    usage_area_id INT,

    -- MaStR-Nummer der EEG-Anlage
    eeg_registration_number VARCHAR,

    wkb_geometry GEOMETRY(POINT, 4326)
);


-- INDEX
CREATE INDEX IF NOT EXISTS idx_unit_solar_municipality_key ON de_solar_units (municipality_key);

-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_unq_solar_unit_reg_num ON de_solar_units (unit_registration_number);

-- GEOMETRY INDEX
CREATE INDEX IF NOT EXISTS idx_solar_unit_geometry ON de_solar_units USING GIST (wkb_geometry);
