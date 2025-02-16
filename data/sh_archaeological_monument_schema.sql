-- TABELLE ARCHÄOLOGISCHER KULTURDENKMALE SCHLESWIG-HOLSTEIN
DROP TABLE IF EXISTS sh_archaeological_monument CASCADE;

CREATE TABLE IF NOT EXISTS sh_archaeological_monument (
    id SERIAL PRIMARY KEY,
    proper_name TEXT,
    object_number VARCHAR(50) NOT NULL,
    district_name TEXT,
    municipality_name TEXT,
    object_description TEXT,
    object_significance TEXT,
    protection_scope TEXT,
    date_registered TIMESTAMP WITH TIME ZONE,
    date_modified TIMESTAMP WITH TIME ZONE,
    status TEXT,
    heritage_authority TEXT,
    municipality_key VARCHAR(8),
    wkb_geometry GEOMETRY(MULTIPOLYGON, 4326)
);


-- HILFSTABELLE KATEGORIEN ARCHÄOLOGISCHER KULTURDENKMALE
DROP TABLE IF EXISTS sh_archaeological_monument_category CASCADE;

CREATE TABLE IF NOT EXISTS sh_archaeological_monument_category (
  id SERIAL PRIMARY KEY,
  label VARCHAR
);


-- TABELLE RELATIONEN KATEGORIE/ARCHÄOLOGISCHES KULTURDENKMAL
DROP TABLE IF EXISTS sh_archaeological_monument_x_category CASCADE;

CREATE TABLE IF NOT EXISTS sh_archaeological_monument_x_category (
  category_id INT NOT NULL,
  monument_id INT NOT NULL,
  FOREIGN KEY(monument_id) REFERENCES sh_archaeological_monument(id),
  FOREIGN KEY(category_id) REFERENCES sh_archaeological_monument_category(id)
);



-- INDEX
CREATE INDEX IF NOT EXISTS idx_sh_archaeological_monument_object_number ON sh_archaeological_monument (object_number);
CREATE INDEX IF NOT EXISTS idx_sh_archaeological_monument_municipality_key ON sh_archaeological_monument (municipality_key);
CREATE INDEX IF NOT EXISTS idx_sh_archaeological_monument_date_registered ON sh_archaeological_monument (date_registered);
CREATE INDEX IF NOT EXISTS idx_sh_archaeological_monument_date_modified ON sh_archaeological_monument (date_modified);

-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_uniq_sh_archaeological_monument_category_label ON sh_archaeological_monument_category (label);
CREATE UNIQUE INDEX IF NOT EXISTS idx_uniq_sh_archaeological_monument_category ON sh_archaeological_monument_x_category (monument_id, category_id);

-- GEOMETRY INDEX
CREATE INDEX IF NOT EXISTS idx_gist_sh_archaeological_monument_geometry ON sh_archaeological_monument USING GIST (wkb_geometry);
