#!/bin/bash
set -e

HOST="rabbitmq"
PORT="5672"

echo "Esperando a que RabbitMQ esté disponible en $HOST:$PORT ..."
until nc -z "$HOST" "$PORT"; do
  echo "RabbitMQ no está listo - esperando..."
  sleep 2
done

echo "RabbitMQ está listo. Iniciando consumidor..."
exec "$@"
