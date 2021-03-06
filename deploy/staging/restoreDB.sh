#!/bin/bash

set -e
set -u

export DBHOST=localhost
export DBPORT=5432

psql \
    -X \
    -U postgres \
    password=admin \
    -h $DBHOST \
    -f /var/www/is2/deploy/staging/scripSql.sql \
    --echo-all \
    --set AUTOCOMMIT=off \
    --set ON_ERROR_STOP=on \
    --set VERBOSITY=verbose \
    --set PGPASSWORD='admin' \
    --set PGOPTIONS='--client-min-messages=warning' \


PGPASSWORD="admin" /usr/bin/pg_restore --host "localhost" --port "5432" --username "postgres" --dbname "is2_g8_db" --verbose "/home/$USER/copia"

echo "sql script successful"
exit 0

