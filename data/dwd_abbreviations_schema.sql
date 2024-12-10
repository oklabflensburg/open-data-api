-- HILFSTABELLE DWD ABKÜRZUNGEN
DROP TABLE IF EXISTS de_weather_abbreviation CASCADE;

CREATE TABLE IF NOT EXISTS de_weather_abbreviation (
    id SERIAL PRIMARY KEY,
    abbreviation_code VARCHAR NOT NULL,
    abbreviation_label VARCHAR
);

INSERT INTO de_weather_abbreviation (abbreviation_code, abbreviation_label) VALUES
('STAT_NAME', 'Stationsname'),
('STAT_ID', 'Stations_ID'),
('KE', 'Kennung'),
('STAT', 'Stationskennung'),
('BR_HIGH', 'Breite'),
('LA_HIGH', 'Länge'),
('HS', 'Stationshöhe in Metern über NN auf Höhe des Klimagartens bezogen (Ausnahme: KE=SO: Höhe des Aufstellungsortes des Sonnenscheinschreibers)'),
('HFG_NFG', 'Flussgebiet (Haupt- und Nebenflussgebiete)'),
('BL', 'Bundesland'),
('BEGINN', 'Beginn der Datenreihe'),
('ENDE', 'Ende der Datenreihe');



-- HILFSTABELLE DWD STATIONSKENNUNGEN
DROP TABLE IF EXISTS de_weather_station_code CASCADE;

CREATE TABLE IF NOT EXISTS de_weather_station_code (
    id SERIAL PRIMARY KEY,
    station_code VARCHAR NOT NULL,
    station_label VARCHAR
);


INSERT INTO de_weather_station_code (station_code, station_label) VALUES
('AE', 'Stationen mit aerologischen Beobachtungen'),
('EB', 'Stationen mit täglichen Daten der Erdbodentemperatur'),
('FF', 'Stationen mit stündlichen Winddaten'),
('KL', 'Stationen mit Klimadaten'),
('MI', 'Stationen mit automatischen Messungen (10-Minuten-Auflösung)'),
('MN', 'Stationen mit automatischen Messungen (10-Minuten-Auflösung)'),
('PE', 'Stationen mit phänologischen Beobachtungen'),
('PS', 'Stationen mit phänologischen Beobachtungen'),
('RR', 'Stationen mit täglichen Niederschlagsdaten'),
('SO', 'Stationen mit stündlichen Daten der Sonnenscheindauer'),
('SY', 'Stationen mit stündlichen, automatischen Messungen (teilweise ergänzt mit Augenbeobachtungen, vor Einführung der Automaten nur Augenbeobachtungen)'),
('TU', 'Stationen mit stündlichen Daten der Temperatur und der relativen Feuchte');

