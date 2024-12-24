FROM postgres:14

COPY postgres.conf /etc/postgresql/postgresql.conf
COPY init_replica.sh /docker-entrypoint-initdb.d/

EXPOSE 5432
