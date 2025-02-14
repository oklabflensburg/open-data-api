-- TABELLE ARCHÄOLOGISCHER KULTURDENKMALE SCHLESWIG-HOLSTEIN
DROP TABLE IF EXISTS sh_archaeological_monument CASCADE;

CREATE TABLE IF NOT EXISTS sh_archaeological_monument (
    id SERIAL PRIMARY KEY,
    object_name TEXT NOT NULL,
    proper_name TEXT,
    object_number VARCHAR(50) UNIQUE NOT NULL,
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

-- INDEX
CREATE INDEX IF NOT EXISTS idx_sh_archaeological_monument_municipality_key ON sh_archaeological_monument (municipality_key);

-- UNIQUE INDEX
CREATE UNIQUE INDEX IF NOT EXISTS idx_unq_sh_archaeological_monument_object_number ON sh_archaeological_monument (object_number);

-- GEOMETRY INDEX
CREATE INDEX IF NOT EXISTS idx_gist_sh_archaeological_monument_geometry ON sh_archaeological_monument USING GIST (wkb_geometry);
