DROP DATABASE IF EXISTS is2_g8_db;

CREATE DATABASE is2_g8_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_PY.UTF-8'
    LC_CTYPE = 'es_PY.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
