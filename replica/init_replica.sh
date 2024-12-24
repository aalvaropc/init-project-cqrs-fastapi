#!/bin/bash
set -e

until pg_isready -h "$PG_PRIMARY_HOST" -p "$PG_PRIMARY_PORT" -U "$PG_REP_USER"; do
  echo "Esperando a que pg_primary esté listo..."
  sleep 2
done

echo "El primario está listo, iniciando configuración de la réplica..."

rm -rf /var/lib/postgresql/data/*

export PGPASSWORD="$PG_REP_PASSWORD"

pg_basebackup -h "$PG_PRIMARY_HOST" -p "$PG_PRIMARY_PORT" -U "$PG_REP_USER" \
  -D /var/lib/postgresql/data -Fp -Xs -P -R

if [ ! -f /var/lib/postgresql/data/standby.signal ]; then
  echo "Creando archivo standby.signal manualmente..."
  touch /var/lib/postgresql/data/standby.signal
  chown postgres:postgres /var/lib/postgresql/data/standby.signal
fi

{
  echo "# Líneas específicas de replicación en réplica - SCRAM"
  echo "host replication $PG_REP_USER 0.0.0.0/0 scram-sha-256"
} >> /var/lib/postgresql/data/pg_hba.conf

echo "Configuración de la réplica completada."
