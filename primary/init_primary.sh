#!/bin/bash
set -e


cp /etc/postgresql/postgresql.conf /var/lib/postgresql/data/postgresql.conf
chown postgres:postgres /var/lib/postgresql/data/postgresql.conf

psql -U postgres -c "CREATE ROLE $PG_REP_USER REPLICATION LOGIN ENCRYPTED PASSWORD '$PG_REP_PASSWORD';"

{
  echo "# Líneas específicas de replicación (para replicator) - SCRAM"
  echo "host replication $PG_REP_USER 0.0.0.0/0 scram-sha-256"
} >> /var/lib/postgresql/data/pg_hba.conf

psql -U postgres -c "ALTER ROLE $PG_REP_USER PASSWORD '$PG_REP_PASSWORD';"
